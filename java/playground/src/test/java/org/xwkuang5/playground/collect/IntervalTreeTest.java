package org.xwkuang5.playground.collect;

import static com.google.common.truth.Truth.assertThat;

import com.google.common.collect.ImmutableList;
import com.google.common.collect.Range;
import java.util.function.Consumer;
import org.junit.jupiter.api.Test;
import org.xwkuang5.playground.collect.IntervalTree.TreeNode;

public final class IntervalTreeTest {

	private static class IntervalTreeVisitor {

		private static <K, V extends Comparable<V>> void visit(TreeNode<K, V> root,
				Consumer<? super TreeNode<K, V>> consumer) {
			if (root == null) {
				return;
			}
			visit(root.getLeft(), consumer);
			consumer.accept(root);
			visit(root.getRight(), consumer);
		}

		private IntervalTreeVisitor() {
		}
	}

	private static <T> ImmutableList<T> traverse(TreeNode<T, ?> root) {
		ImmutableList.Builder<T> results = ImmutableList.builder();
		IntervalTreeVisitor.visit(root, node -> results.add(node.getKey()));
		return results.build();
	}

	private static void validateTreeHeights(TreeNode<?, ?> root) {
		IntervalTreeVisitor.visit(root, node -> {
			int leftHeight = node.getLeft() == null ? 0 : node.getLeft().getHeight();
			int rightHeight = node.getRight() == null ? 0 : node.getRight().getHeight();
			assertThat(Math.abs(leftHeight - rightHeight) <= 1);
			assertThat(node.getHeight()).isEqualTo(Math.max(leftHeight, rightHeight) + 1);
		});
	}

	@Test
	public void treeNode_rotateLeft() {
		var root = new TreeNode<String, Integer>(null, "a", Range.singleton(1));
		var left = root.insert("b", Range.singleton(0));
		var leftLeft = left.insert("c", Range.singleton(-1));

		var newRoot = root.rotateLeft();

		assertThat(newRoot.getKey()).isEqualTo("b");
		assertThat(newRoot.getHeight()).isEqualTo(2);
		assertThat(newRoot.getLeft()).isEqualTo(leftLeft);
		assertThat(newRoot.getLeft().getHeight()).isEqualTo(1);
		assertThat(newRoot.getRight()).isEqualTo(root);
		assertThat(newRoot.getRight().getHeight()).isEqualTo(1);
	}

	@Test
	public void treeNode_rotateRight() {
		var root = new TreeNode<String, Integer>(null, "a", Range.singleton(1));
		var right = root.insert("b", Range.singleton(2));
		var rightRight = right.insert("c", Range.singleton(3));

		var newRoot = root.rotateRight();

		assertThat(newRoot.getKey()).isEqualTo("b");
		assertThat(newRoot.getHeight()).isEqualTo(2);
		assertThat(newRoot.getLeft()).isEqualTo(root);
		assertThat(newRoot.getLeft().getHeight()).isEqualTo(1);
		assertThat(newRoot.getRight()).isEqualTo(rightRight);
		assertThat(newRoot.getRight().getHeight()).isEqualTo(1);
	}

	@Test
	public void intervalTree_insert() {
		var tree = new IntervalTree<String, Integer>();
		tree.insert("a", Range.singleton(1));
		tree.insert("b", Range.singleton(0));
		tree.insert("c", Range.singleton(-1));
		tree.insert("d", Range.singleton(2));
		tree.insert("e", Range.singleton(3));
		tree.insert("f", Range.singleton(4));
		tree.insert("g", Range.singleton(-2));

		assertThat(traverse(tree.getRoot())).containsExactly("g", "c", "b", "a", "d", "e", "f")
				.inOrder();
		validateTreeHeights(tree.getRoot());
	}

	@Test
	public void intervalTree_insertWithDuplicates() {
		var tree = new IntervalTree<String, Integer>();
		tree.insert("a", Range.singleton(1));
		tree.insert("b", Range.singleton(0));
		tree.insert("c", Range.singleton(-1));
		tree.insert("d", Range.singleton(2));
		tree.insert("e", Range.singleton(3));
		tree.insert("f", Range.singleton(4));
		tree.insert("g", Range.singleton(-2));
		tree.insert("h", Range.singleton(1));
		tree.insert("i", Range.singleton(0));

		assertThat(traverse(tree.getRoot())).containsExactly("g", "c", "i", "b", "h", "a", "d", "e",
				"f").inOrder();
		validateTreeHeights(tree.getRoot());
	}

	@Test
	public void intervalTree_noOverlap() {
		var tree = new IntervalTree<String, Integer>();

		tree.insert("a", Range.closedOpen(1, 2));
		tree.insert("b", Range.closedOpen(3, 4));

		assertThat(tree.overlapping(0)).isEmpty();
		assertThat(tree.overlapping(2)).isEmpty();
		assertThat(tree.overlapping(4)).isEmpty();
		validateTreeHeights(tree.getRoot());
	}

	@Test
	public void intervalTree_pointOverlap() {
		var tree = new IntervalTree<String, Integer>();

		tree.insert("a", 1);
		tree.insert("b", 3);
		tree.insert("c", 5);

		assertThat(tree.overlapping(1)).containsExactly("a");
		assertThat(tree.overlapping(3)).containsExactly("b");
		assertThat(tree.overlapping(5)).containsExactly("c");
		validateTreeHeights(tree.getRoot());
	}

	@Test
	public void intervalTree_rangeOverlap() {
		var tree = new IntervalTree<String, Integer>();

		tree.insert("a", Range.closedOpen(1, 2));
		tree.insert("b", Range.closedOpen(3, 4));
		tree.insert("c", Range.closedOpen(5, 6));

		assertThat(tree.overlapping(Range.closedOpen(0, 2))).containsExactly("a");
		assertThat(tree.overlapping(Range.closedOpen(2, 4))).containsExactly("b");
		assertThat(tree.overlapping(Range.closedOpen(4, 6))).containsExactly("c");

		assertThat(tree.overlapping(Range.closedOpen(0, 4))).containsExactly("a", "b");
		assertThat(tree.overlapping(Range.closedOpen(0, 5))).containsExactly("a", "b");

		assertThat(tree.overlapping(Range.closedOpen(2, 6))).containsExactly("b", "c");

		assertThat(tree.overlapping(Range.closedOpen(0, 6))).containsExactly("a", "b", "c");

		validateTreeHeights(tree.getRoot());
	}

	@Test
	public void intervalTree_rangeOverlapsAll() {
		var tree = new IntervalTree<String, Integer>();

		tree.insert("a", Range.closedOpen(1, 10));
		tree.insert("b", Range.closedOpen(3, 4));
		tree.insert("c", Range.closedOpen(5, 6));

		assertThat(tree.overlapping(Range.closedOpen(0, 2))).containsExactly("a");
		assertThat(tree.overlapping(Range.closedOpen(2, 4))).containsExactly("a", "b");
		assertThat(tree.overlapping(Range.closedOpen(4, 6))).containsExactly("a", "c");

		assertThat(tree.overlapping(Range.closedOpen(0, 6))).containsExactly("a", "b", "c");

		validateTreeHeights(tree.getRoot());
	}
}
