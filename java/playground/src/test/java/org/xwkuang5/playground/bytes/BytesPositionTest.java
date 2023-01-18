package org.xwkuang5.playground.bytes;

import static com.google.common.truth.Truth.assertThat;

import java.util.ArrayList;
import org.junit.jupiter.api.Test;

import static org.junit.Assert.assertThrows;

public final class BytesPositionTest {

	@Test
	public void compareTo() {
		ComparisonTesterBuilder.<BytesPosition>builder()
				.addEqualityGroup(BytesPosition.create(new byte[]{0x01}))
				.addEqualityGroup(BytesPosition.create(new byte[]{0x01, 0x02}))
				.addEqualityGroup(BytesPosition.create(new byte[]{0x01, 0x02, 0x03}))
				.addEqualityGroup(BytesPosition.successor(new byte[]{0x01}))
				.addEqualityGroup(BytesPosition.create(new byte[]{0x02}))
				.addEqualityGroup(BytesPosition.create(new byte[]{0x02, 0x01}))
				.addEqualityGroup(BytesPosition.successor(new byte[]{0x02, 0x01}))
				.addEqualityGroup(BytesPosition.create(new byte[]{0x02, 0x02, 0x02}))
				.addEqualityGroup(BytesPosition.successor(new byte[]{0x03}))
				.test();
	}

	@Test
	public void comparisonTesterBuilder() {
		ComparisonTesterBuilder.<Integer>builder()
				.addEqualityGroup(1)
				.addEqualityGroup(2)
				.addEqualityGroup(3)
				.addEqualityGroup(4)
				.addEqualityGroup(5)
				.test();
	}

	@Test
	public void comparisonTesterBuilder_unorderedEqualityGroups_throws() {
		var tester =
				ComparisonTesterBuilder.<Integer>builder()
						.addEqualityGroup(5)
						.addEqualityGroup(4)
						.addEqualityGroup(3)
						.addEqualityGroup(2)
						.addEqualityGroup(1);
		assertThrows(AssertionError.class, tester::test);
	}


	private static class ComparisonTesterBuilder<T extends Comparable<T>> {

		private final ArrayList<T> equalityGroups;

		ComparisonTesterBuilder<T> addEqualityGroup(T t) {
			equalityGroups.add(t);

			return this;
		}

		void test() {
			for (int i = 0; i < equalityGroups.size(); ++i) {
				for (int j = i + 1; j < equalityGroups.size(); ++j) {
					var left = equalityGroups.get(i);
					var right = equalityGroups.get(j);
					assertThat(left).isLessThan(right);
				}
			}
		}

		static <T extends Comparable<T>> ComparisonTesterBuilder<T> builder() {
			return new ComparisonTesterBuilder<T>();
		}

		private ComparisonTesterBuilder() {
			this.equalityGroups = new ArrayList<>();
		}
	}
}
