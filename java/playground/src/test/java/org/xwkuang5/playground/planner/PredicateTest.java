package org.xwkuang5.playground.planner;

import static org.junit.Assert.assertThrows;
import static com.google.common.truth.Truth.assertThat;
import static org.xwkuang5.playground.planner.Predicate.not;
import static org.xwkuang5.playground.planner.Predicate.and;
import static org.xwkuang5.playground.planner.Predicate.or;

import com.google.common.collect.ImmutableSet;
import org.junit.jupiter.api.Test;

public final class PredicateTest {

	private static Predicate A = Predicate.literal("a");
	private static Predicate B = Predicate.literal("b");
	private static Predicate C = Predicate.literal("c");

	private static Predicate NOT_A = not(Predicate.literal("a"));
	private static Predicate NOT_B = not(Predicate.literal("b"));
	private static Predicate NOT_C = not(Predicate.literal("c"));

	@Test
	public void and_empty_throws() {
		assertThrows(IllegalArgumentException.class, () -> and(ImmutableSet.of()));
	}

	@Test
	public void or_empty_throws() {
		assertThrows(IllegalArgumentException.class, () -> and(ImmutableSet.of()));
	}

	// TODO(louiskuang): Add more complicated test cases around negation and more deeply nested trees.
	@Test
	public void cnf() {
		assertThat(A.toCnf()).isEqualTo(and(or(A)));

		assertThat(and(A, B).toCnf()).isEqualTo(and(or(A), or(B)));
		assertThat(and(B, A).toCnf()).isEqualTo(and(or(A), or(B)));
		assertThat(or(A, B).toCnf()).isEqualTo(and(or(A, B)));

		assertThat(and(A, and(B, C)).toCnf()).isEqualTo(and(or(A), or(B), or(C)));
		assertThat(and(A, or(B, C)).toCnf()).isEqualTo(and(or(A), or(B, C)));
		assertThat(or(A, or(B, C)).toCnf()).isEqualTo(and(or(A, B, C)));
		assertThat(or(A, and(B, C)).toCnf()).isEqualTo(and(or(A, B), or(A, C)));

		assertThat(or(and(A, B), and(A, C)).toCnf()).isEqualTo(
				and(or(A), or(A, C), or(A, B), or(B, C)));

		assertThat(not(and(A, B)).toCnf()).isEqualTo(and(or(NOT_A, NOT_B)));
		assertThat(not(or(A, B)).toCnf()).isEqualTo(and(or(NOT_A), or(NOT_B)));
	}

	@Test
	public void dnf() {
		assertThat(A.toDnf()).isEqualTo(or(and(A)));

		assertThat(and(A, B).toDnf()).isEqualTo(or(and(A, B)));
		assertThat(and(B, A).toDnf()).isEqualTo(or(and(A, B)));
		assertThat(or(A, B).toDnf()).isEqualTo(or(and(A), and(B)));

		assertThat(and(A, and(B, C)).toDnf()).isEqualTo(or(and(A, B, C)));
		assertThat(and(A, or(B, C)).toDnf()).isEqualTo(or(and(A, B), and(A, C)));
		assertThat(or(A, or(B, C)).toDnf()).isEqualTo(or(and(A), and(B), and(C)));
		assertThat(or(A, and(B, C)).toDnf()).isEqualTo(or(and(A), and(B, C)));

		assertThat(and(or(A, B), or(A, C)).toDnf()).isEqualTo(
				or(and(A), and(A, C), and(A, B), and(B, C)));

		assertThat(not(and(A, B)).toDnf()).isEqualTo(or(and(NOT_A), and(NOT_B)));
		assertThat(not(or(A, B)).toDnf()).isEqualTo(or(and(NOT_A, NOT_B)));
	}
}
