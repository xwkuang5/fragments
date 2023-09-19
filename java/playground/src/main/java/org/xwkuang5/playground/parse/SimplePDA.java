package org.xwkuang5.playground.parse;

import static com.google.common.base.Preconditions.checkState;

import com.google.auto.value.AutoOneOf;
import com.google.common.collect.ImmutableList;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.Stack;
import java.util.Vector;
import java.util.stream.Collectors;

/**
 * A simple pushdown automata that recognizes the 0^n1^n text book context free language.
 *
 * <p>Instead of simply using a single stack to consume encountered zeros, we will use the general
 * CFG -> PDA proof implementation.
 *
 * <p>The implicit rules are as follows: <pre>{@code
 * S -> 0R1
 * R -> S | epsilon
 * }</pre>
 */
public final class SimplePDA {

	// Since we are hardcoding the transitions, it suffices to represent the variable.
	enum Variable {
		S, R
	}

	@AutoOneOf(Symbol.Type.class)
	public abstract static class Symbol {

		enum Type {
			TERMINAL, VARIABLE
		}

		public abstract Type type();

		public abstract char terminal();

		public abstract Variable variable();

		public boolean isTerminal() {
			return type().equals(Type.TERMINAL);
		}

		public boolean isVariable() {
			return type().equals(Type.VARIABLE);
		}

		public static Symbol ofTerminal(char c) {
			return AutoOneOf_SimplePDA_Symbol.terminal(c);
		}

		public static Symbol ofVariable(Variable v) {
			return AutoOneOf_SimplePDA_Symbol.variable(v);
		}
	}

	private List<Stack<Symbol>> stacks;

	private SimplePDA() {
		this.stacks = initStack();
	}

	private static List<Stack<Symbol>> initStack() {
		return replaceVariable(Variable.S).stream().map(ImmutableList::reverse)
				.map(reversedExpansion -> {
					Stack<Symbol> symbols = new Stack<>();
					reversedExpansion.forEach(symbols::push);
					return symbols;
				}).collect(Collectors.toList());
	}

	/**
	 * Recursively replaces the top of the stack with the derivation if it is a variable type.
	 */
	private void advance(char c) {
		List<Stack<Symbol>> newStacks = new ArrayList<>();

		for (Stack<Symbol> cur : stacks) {
			advanceStack(cur, c).ifPresent(newStacks::addAll);
		}

		this.stacks = newStacks;
	}

	private static Optional<List<Stack<Symbol>>> advanceStack(Stack<Symbol> stack, char c) {
		if (stack.isEmpty()) {
			return Optional.empty();
		}

		Symbol top = stack.pop();
		checkState(top.isTerminal());

		if (top.terminal() != c) {
			return Optional.empty();
		}

		List<Stack<Symbol>> threads = new ArrayList<>();
		threads.add(stack);
		boolean madeProgress = true;
		// This loop has an assumption that the grammar will not expand into an infinite loop when substituting variables.
		while (madeProgress) {
			List<Stack<Symbol>> newThreads = new ArrayList<>();
			madeProgress = false;
			// for each active threads, try to advance it so that the stack either becomes empty or the top of the stack is a terminal.
			for (var thread : threads) {
				if (thread.isEmpty()) {
					newThreads.add(thread);
					continue;
				}
				Symbol head = thread.peek();
				if (head.isTerminal()) {
					newThreads.add(thread);
					continue;
				}
				head = thread.pop();
				var replacements = replaceVariable(head.variable());
				checkState(!replacements.isEmpty());
				madeProgress = true;
				// for each replacement, fork the current thread and push the replacement onto the thread
				for (var sequence : replacements) {
					Stack<Symbol> newThread = (Stack<Symbol>) thread.clone();
					sequence.reverse().forEach(newThread::push);
					newThreads.add(newThread);
				}
			}
			if (madeProgress) {
				threads = newThreads;
			}
		}

		return Optional.of(threads);
	}

	private static ImmutableList<ImmutableList<Symbol>> replaceVariable(Variable variable) {
		return switch (variable) {
			case R ->
					ImmutableList.of(ImmutableList.of(Symbol.ofVariable(Variable.S)), ImmutableList.of());
			case S -> ImmutableList.of(
					ImmutableList.of(Symbol.ofTerminal('0'), Symbol.ofVariable(Variable.R),
							Symbol.ofTerminal('1')));
		};
	}

	/**
	 * Returns {@code true} if {@code input} is a string in the language.
	 *
	 * @param input ASCII-only string
	 */
	public static boolean match(String input) {
		if (input.isEmpty()) {
			return true;
		}

		var pda = new SimplePDA();

		for (int i = 0; i < input.length(); i++) {
			pda.advance(input.charAt(i));

			// If at any point there's no more active threads remaining, short-circuit and reject.
			if (pda.stacks.isEmpty()) {
				return false;
			}
		}

		if (pda.stacks.isEmpty()) {
			return false;
		}
		return pda.stacks.stream().anyMatch(Vector::isEmpty);
	}

	public static void main(String[] args) {
	}
}
