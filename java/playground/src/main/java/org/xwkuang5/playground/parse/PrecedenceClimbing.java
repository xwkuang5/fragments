package org.xwkuang5.playground.parse;

import static com.google.common.base.Preconditions.checkArgument;
import static com.google.common.base.Preconditions.checkState;

import com.google.auto.value.AutoOneOf;
import com.google.common.collect.Iterators;
import com.google.common.collect.PeekingIterator;
import java.util.Iterator;
import java.util.stream.IntStream;
import org.xwkuang5.playground.parse.PrecedenceClimbing.Atom.Type;

/**
 * A simple arithmetic expression parser that handles parentheses, operator precedence and
 * associativity.
 *
 * <p>Associativity is handled by bumping their precedence to precede over other operators of the
 * same precedence (technically a fractional bump is enough).
 *
 * <p>Parentheses are handled by treating the sub-expressions that they represent as a single value
 * that need to be evaluated before anything else.
 *
 * <p><a
 * href="https://eli.thegreenplace.net/2012/08/02/parsing-expressions-by-precedence-climbing">Reference</a>
 */
final class PrecedenceClimbing {

	enum Associativity {
		LEFT, RIGHT
	}

	/**
	 * Binary operator
	 */
	enum Operator {
		PLUS(1, Associativity.LEFT), MINUS(1, Associativity.LEFT), MULTIPLY(2,
				Associativity.LEFT), DIVIDE(2, Associativity.LEFT), EXP(3, Associativity.RIGHT), LEFT_PAREN(
				100, Associativity.LEFT), RIGHT_PAREN(100, Associativity.LEFT);

		static final int MINIMUM_PRECEDENCE = 0;

		final int precedence;
		final Associativity associativity;

		Operator(int precedence, Associativity associativity) {
			this.precedence = precedence;
			this.associativity = associativity;
		}
	}

	@AutoOneOf(Atom.Type.class)
	abstract static class Atom {

		enum Type {
			VALUE, OPERATOR
		}

		abstract Type type();

		abstract int value();

		abstract Operator operator();

		static Atom op(Operator operator) {
			return AutoOneOf_PrecedenceClimbing_Atom.operator(operator);
		}

		static Atom value(int value) {
			return AutoOneOf_PrecedenceClimbing_Atom.value(value);
		}
	}

	static int evaluate(Iterable<Atom> atoms) {
		return evaluate(Operator.MINIMUM_PRECEDENCE, Iterators.peekingIterator(atoms.iterator()));
	}

	private static int evaluate(int minimumPrecedence, PeekingIterator<Atom> atoms) {
		int result = consumeValue(atoms);

		while (atoms.hasNext()) {
			var nextAtom = atoms.peek();
			checkArgument(nextAtom.type().equals(Type.OPERATOR),
					"expected atom of operator type but got %s", nextAtom);
			checkState(!nextAtom.operator().equals(Operator.LEFT_PAREN));
			if (nextAtom.operator().equals(Operator.RIGHT_PAREN)
					|| nextAtom.operator().precedence < minimumPrecedence) {
				break;
			}

			nextAtom = atoms.next();

			int nextPrecedence =
					nextAtom.operator().precedence;
			if (nextAtom.operator().associativity.equals(
					Associativity.LEFT)) {
				nextPrecedence += 1;
			}

			int nextExpressionValue = evaluate(nextPrecedence, atoms);

			result = evaluateBinaryOp(nextAtom.operator(), result, nextExpressionValue);
		}

		return result;
	}

	private static int evaluateBinaryOp(Operator op, int left, int right) {
		return switch (op) {
			case PLUS -> left + right;
			case MINUS -> left - right;
			case MULTIPLY -> left * right;
			case DIVIDE -> left / right;
			case EXP -> IntStream.generate(() -> left).limit(right).reduce((l, r) -> l * r).orElseThrow();
			// fall through
			case LEFT_PAREN, RIGHT_PAREN -> throw new IllegalStateException("ah oh");
		};
	}

	private static int consumeValue(Iterator<Atom> atoms) {
		checkArgument(atoms.hasNext(), "can not consume value from an empty iterator");
		var atom = atoms.next();
		switch (atom.type()) {
			case VALUE:
				return atom.value();
			case OPERATOR: {
				if (atom.operator().equals(Operator.LEFT_PAREN)) {
					int result = evaluate(0, Iterators.peekingIterator(atoms));
					checkArgument(atoms.hasNext());
					checkArgument(atoms.next().operator().equals(Operator.RIGHT_PAREN));
					return result;
				}
				throw new IllegalArgumentException(
						String.format("expected atom of value type but got %s", atom));
			}
		}
		throw new AssertionError("impossible");
	}
}
