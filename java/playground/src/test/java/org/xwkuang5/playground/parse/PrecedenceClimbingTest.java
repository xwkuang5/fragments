package org.xwkuang5.playground.parse;

import static org.junit.Assert.assertThrows;
import static com.google.common.truth.Truth.assertThat;
import static org.xwkuang5.playground.parse.PrecedenceClimbing.evaluate;
import static org.xwkuang5.playground.parse.PrecedenceClimbing.Atom.value;
import static org.xwkuang5.playground.parse.PrecedenceClimbing.Atom.op;

import com.google.common.collect.ImmutableList;
import org.junit.jupiter.api.Test;
import org.xwkuang5.playground.parse.PrecedenceClimbing.Operator;

final class PrecedenceClimbingTest {

	@Test
	public void operatorAndOperandDoNotMatch() {
		assertThrows(IllegalArgumentException.class,
				() -> evaluate(ImmutableList.of(value(1), value(2))));

		assertThrows(IllegalArgumentException.class,
				() -> evaluate(ImmutableList.of(value(1), op(Operator.PLUS), op(Operator.PLUS))));
	}

	@Test
	public void singleValue() {
		assertThat(evaluate(ImmutableList.of(value(1)))).isEqualTo(1);
	}

	@Test
	public void singleValue_parenthesis() {
		assertThat(evaluate(
				ImmutableList.of(op(Operator.LEFT_PAREN), value(1), op(Operator.RIGHT_PAREN)))).isEqualTo(
				1);
	}

	@Test
	public void singleValue_parentheses() {
		assertThat(evaluate(
				ImmutableList.of(op(Operator.LEFT_PAREN), op(Operator.LEFT_PAREN), value(1),
						op(Operator.RIGHT_PAREN), op(Operator.RIGHT_PAREN)))).isEqualTo(
				1);
	}

	@Test
	public void plus() {
		assertThat(evaluate(ImmutableList.of(value(1), op(Operator.PLUS), value(1)))).isEqualTo(2);
		assertThat(evaluate(ImmutableList.of(value(1), op(Operator.PLUS), value(1), op(Operator.PLUS),
				value(1)))).isEqualTo(3);
	}

	@Test
	public void plus_parenthesis() {
		assertThat(evaluate(
				ImmutableList.of(value(1), op(Operator.PLUS), op(Operator.LEFT_PAREN), value(1),
						op(Operator.PLUS),
						value(1), op(Operator.RIGHT_PAREN)))).isEqualTo(3);
	}

	@Test
	public void minus() {
		assertThat(evaluate(ImmutableList.of(value(1), op(Operator.MINUS), value(1)))).isEqualTo(0);
		assertThat(evaluate(ImmutableList.of(value(1), op(Operator.MINUS), value(1), op(Operator.MINUS),
				value(1)))).isEqualTo(-1);
	}

	@Test
	public void multiply() {
		assertThat(evaluate(ImmutableList.of(value(2), op(Operator.MULTIPLY), value(2)))).isEqualTo(4);
		assertThat(evaluate(
				ImmutableList.of(value(2), op(Operator.MULTIPLY), value(2), op(Operator.MULTIPLY),
						value(3)))).isEqualTo(12);
	}

	@Test
	public void divide() {
		assertThat(evaluate(ImmutableList.of(value(2), op(Operator.DIVIDE), value(2)))).isEqualTo(1);
		assertThat(evaluate(
				ImmutableList.of(value(2), op(Operator.DIVIDE), value(2), op(Operator.DIVIDE),
						value(2)))).isEqualTo(0);
	}

	@Test
	public void exponent() {
		assertThat(evaluate(ImmutableList.of(value(2), op(Operator.EXP), value(2)))).isEqualTo(4);
		assertThat(evaluate(ImmutableList.of(value(2), op(Operator.EXP), value(2), op(Operator.EXP),
				value(3)))).isEqualTo(256);
	}

	@Test
	public void mixed() {
		assertThat(evaluate(
				ImmutableList.of(value(2), op(Operator.PLUS), value(2), op(Operator.MULTIPLY), value(10),
						op(Operator.DIVIDE), value(2), op(Operator.EXP), value(2), op(Operator.MINUS),
						value(1)))).isEqualTo(6);

		assertThat(evaluate(
				ImmutableList.of(value(2), op(Operator.PLUS), value(2), op(Operator.MULTIPLY),
						op(Operator.LEFT_PAREN), value(10),
						op(Operator.DIVIDE), value(2), op(Operator.RIGHT_PAREN), op(Operator.EXP), value(2),
						op(Operator.MINUS),
						value(1)))).isEqualTo(51);

		assertThat(evaluate(
				ImmutableList.of(value(2), op(Operator.PLUS), op(Operator.LEFT_PAREN), value(2),
						op(Operator.MULTIPLY),
						op(Operator.LEFT_PAREN), value(10),
						op(Operator.DIVIDE), value(2), op(Operator.RIGHT_PAREN), op(Operator.RIGHT_PAREN),
						op(Operator.EXP), value(2),
						op(Operator.MINUS),
						value(1)))).isEqualTo(101);

		assertThat(evaluate(
				ImmutableList.of(value(2), op(Operator.MINUS), value(10), op(Operator.DIVIDE), value(2),
						op(Operator.MULTIPLY), value(5), op(Operator.EXP), value(1), op(Operator.PLUS),
						value(1)))).isEqualTo(-22);
	}
}
