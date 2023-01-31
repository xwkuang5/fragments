package org.xwkuang5.playground.parse;

import static com.google.common.base.Preconditions.checkArgument;

import com.google.auto.value.AutoOneOf;
import com.google.common.collect.Iterators;
import com.google.common.collect.PeekingIterator;
import java.util.Iterator;
import java.util.stream.IntStream;
import org.xwkuang5.playground.parse.PrecedenceClimbing.Atom.Type;

final class PrecedenceClimbing {

	enum Associativity {
		LEFT, RIGHT
	}

	/**
	 * Binary operator
	 */
	enum Operator {
		PLUS(1, Associativity.LEFT), MINUS(1, Associativity.LEFT), MULTIPLY(2,
				Associativity.LEFT), DIVIDE(2, Associativity.LEFT), EXP(3, Associativity.RIGHT);

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

			if (nextAtom.operator().precedence < minimumPrecedence) {
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
		};
	}

	private static int consumeValue(Iterator<Atom> atoms) {
		checkArgument(atoms.hasNext(), "can not consume value from an empty iterator");
		var atom = atoms.next();
		checkArgument(atom.type().equals(Type.VALUE), "expected atom of value type but got %s", atom);
		return atom.value();
	}
}
