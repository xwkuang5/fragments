package org.xwkuang5.playground.collect;

import static com.google.common.base.Preconditions.checkArgument;
import static com.google.common.base.Preconditions.checkNotNull;
import static com.google.common.base.Preconditions.checkState;

import com.google.common.annotations.VisibleForTesting;
import com.google.common.collect.BoundType;
import com.google.common.collect.ImmutableList;
import com.google.common.collect.Range;
import java.util.function.Consumer;
import javax.annotation.Nullable;

public final class IntervalTree<K, V extends Comparable<V>> {

	@Nullable
	private TreeNode<K, V> root;

	public boolean isEmpty() {
		return root == null;
	}

	public ImmutableList<K> overlapping(Range<V> range) {
		if (root == null) {
			return ImmutableList.of();
		}
		ImmutableList.Builder<K> builder = ImmutableList.builder();
		traverseOverlapping(root, range, builder::add);
		return builder.build();
	}

	public ImmutableList<K> overlapping(V point) {
		return overlapping(Range.singleton(point));
	}

	public void insert(K key, Range<V> range) {
		TreeNode<K, V> inserted;
		if (root == null) {
			inserted = new TreeNode<>(null, key, range);
			root = inserted;
		} else {
			inserted = root.insert(key, range);
		}
		rebalance(inserted);
	}

	public void insert(K key, V point) {
		insert(key, Range.singleton(point));
	}

	public IntervalTree() {
		this.root = null;
	}

	@VisibleForTesting
	TreeNode<K, V> getRoot() {
		return root;
	}

	private void rebalance(TreeNode<K, V> treeNode) {
		TreeNode<K, V> newTreeNode = treeNode;
		int leftHeight = treeNode.left == null ? 0 : treeNode.left.height;
		int rightHeight = treeNode.right == null ? 0 : treeNode.right.height;
		if (leftHeight - rightHeight >= 2) {
			newTreeNode = rebalanceLeft(treeNode);
		} else if (rightHeight - leftHeight >= 2) {
			newTreeNode = rebalanceRight(treeNode);
		}
		if (newTreeNode.isRoot()) {
			root = newTreeNode;
		} else {
			rebalance(newTreeNode.parent);
		}
	}

	private TreeNode<K, V> rebalanceLeft(TreeNode<K, V> treeNode) {
		checkArgument(treeNode.left != null);
		var left = treeNode.left;
		int leftHeight = left.left == null ? 0 : left.left.height;
		int rightHeight = left.right == null ? 0 : left.right.height;
		if (leftHeight > rightHeight) {
			return treeNode.rotateLeft();
		}
		checkState(leftHeight != rightHeight);
		treeNode.left = left.rotateRight();
		return treeNode.rotateLeft();
	}

	private TreeNode<K, V> rebalanceRight(TreeNode<K, V> treeNode) {
		checkArgument(treeNode.right != null);
		var right = treeNode.right;
		int leftHeight = right.left == null ? 0 : right.left.height;
		int rightHeight = right.right == null ? 0 : right.right.height;
		if (rightHeight > leftHeight) {
			return treeNode.rotateRight();
		}
		checkState(leftHeight != rightHeight);
		treeNode.right = right.rotateLeft();
		return treeNode.rotateRight();
	}

	private void traverseOverlapping(TreeNode<K, V> node, Range<V> range,
			Consumer<? super K> consumer) {
		if (node == null) {
			return;
		}
		if (isBefore(range, node.range)) {
			traverseOverlapping(node.left, range, consumer);
		} else {
			traverseOverlapping(node.left, range, consumer);
			if (node.range.isConnected(range) && !node.range.intersection(range).isEmpty()) {
				consumer.accept(node.key);
			}
			traverseOverlapping(node.right, range, consumer);
		}
	}

	/**
	 * Returns {@code true} if {@code left} is before {@code right}.
	 */
	private static <T extends Comparable<T>> boolean isBefore(Range<T> left, Range<T> right) {
		int cmp = left.upperEndpoint().compareTo(right.lowerEndpoint());
		if (cmp < 0) {
			return true;
		} else if (cmp == 0) {
			return left.upperBoundType().equals(BoundType.OPEN);
		}
		return false;
	}

	@VisibleForTesting
	static class TreeNode<K, V extends Comparable<V>> {

		private int height;

		@Nullable
		private TreeNode<K, V> parent;
		@Nullable
		private TreeNode<K, V> left;
		@Nullable
		private TreeNode<K, V> right;
		private final K key;
		private final Range<V> range;

		TreeNode(@Nullable TreeNode<K, V> parent, K key, Range<V> range) {
			this.height = 1;
			this.parent = parent;
			this.left = null;
			this.right = null;
			this.key = key;
			this.range = range;
		}

		private void adjustHeight() {
			int leftHeight = left == null ? 0 : left.height;
			int rightHeight = right == null ? 0 : right.height;
			this.height = Math.max(leftHeight, rightHeight) + 1;
		}

		private boolean isRoot() {
			return parent == null;
		}

		private boolean isLeft() {
			return !isRoot() && parent.left == this;
		}

		private boolean isRight() {
			return !isRoot() && parent.right == this;
		}

		TreeNode<K, V> insert(K key, Range<V> range) {
			TreeNode<K, V> node;
			if (isAfter(range)) {
				if (left == null) {
					node = new TreeNode<>(this, key, range);
					this.left = node;
				} else {
					node = left.insert(key, range);
				}
			} else {
				if (right == null) {
					node = new TreeNode<>(this, key, range);
					this.right = node;
				} else {
					node = right.insert(key, range);
				}
			}
			adjustHeight();
			return node;
		}

		K getKey() {
			return key;
		}

		int getHeight() {
			return height;
		}

		TreeNode<K, V> getLeft() {
			return left;
		}

		TreeNode<K, V> getRight() {
			return right;
		}

		/**
		 * Rotates around the left subtree rooted at {@code this} and returns the new root node.
		 */
		TreeNode<K, V> rotateLeft() {
			checkNotNull(this.left);
			var newRoot = this.left;
			// Update subtree
			this.left = newRoot.right;
			if (newRoot.right != null) {
				newRoot.right.parent = this;
			}
			// Update new root
			newRoot.right = this;
			newRoot.parent = this.parent;

			// Update parent pointer
			if (isLeft()) {
				this.parent.left = newRoot;
			} else if (isRight()) {
				this.parent.right = newRoot;
			}
			this.parent = newRoot;

			this.adjustHeight();
			newRoot.adjustHeight();
			return newRoot;
		}

		/**
		 * Rotates around the right subtree rooted at {@code this} and returns the new root node.
		 */
		TreeNode<K, V> rotateRight() {
			checkNotNull(this.right);
			var newRoot = this.right;
			this.right = newRoot.left;
			if (newRoot.left != null) {
				newRoot.left.parent = this;
			}
			// Update new root
			newRoot.left = this;
			newRoot.parent = this.parent;

			// Update parent pointer
			if (isLeft()) {
				this.parent.left = newRoot;
			} else if (isRight()) {
				this.parent.right = newRoot;
			}
			this.parent = newRoot;

			this.adjustHeight();
			newRoot.adjustHeight();
			return newRoot;
		}

		private boolean isAfter(Range<V> otherRange) {
			int cmp = otherRange.lowerEndpoint().compareTo(this.range.lowerEndpoint());
			if (cmp < 0) {
				return true;
			} else if (cmp == 0) {
				return otherRange.lowerBoundType().equals(this.range.lowerBoundType())
						|| otherRange.lowerBoundType().equals(BoundType.CLOSED);
			}
			return false;
		}
	}
}
