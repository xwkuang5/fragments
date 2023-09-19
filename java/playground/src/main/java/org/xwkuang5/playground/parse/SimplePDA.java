package org.xwkuang5.playground.parse;

import static com.google.common.base.Preconditions.checkState;

import com.google.auto.value.AutoOneOf;
import com.google.common.collect.ImmutableList;
import java.util.ArrayList;
import java.util.List;
import java.util.Stack;
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

	private static class PDAStack {

		private final Stack<Symbol> stack;

		private static PDAStack create(Iterable<Symbol> forwardSymbols) {
			Stack<Symbol> symbols = new Stack<>();
			ImmutableList.copyOf(forwardSymbols).reverse().forEach(symbols::push);
			return new PDAStack(symbols);
		}

		private PDAStack(Stack<Symbol> stack) {
			this.stack = stack;
		}

		private PDAStack fork() {
			Stack<Symbol> cloned = (Stack<Symbol>) stack.clone();
			return new PDAStack(cloned);
		}

		private boolean isAccepting() {
			return stack.isEmpty();
		}

		private boolean canAdvance() {
			return !stack.isEmpty() && !stack.peek().isTerminal();
		}

		private ImmutableList<PDAStack> nonDeterministicallyAdvance() {
			List<PDAStack> threads = new ArrayList<>();
			threads.add(this);
			boolean madeProgress = true;
			// This loop has an assumption that the grammar will not expand into an infinite loop when substituting variables.
			while (madeProgress) {
				List<PDAStack> newThreads = new ArrayList<>();
				madeProgress = false;
				// for each active threads, try to advance it so that the stack either becomes empty or the top of the stack is a terminal.
				for (var thread : threads) {
					if (!thread.canAdvance()) {
						newThreads.add(thread);
						continue;
					}
					var top = thread.stack.pop();
					checkState(top.isVariable());
					var replacements = replaceVariable(top.variable());
					checkState(!replacements.isEmpty());
					madeProgress = true;
					// for each replacement, fork the current thread and push the replacement onto the thread
					for (var sequence : replacements) {
						PDAStack newThread = thread.fork();
						sequence.reverse().forEach(newThread.stack::push);
						newThreads.add(newThread);
					}
				}
				if (madeProgress) {
					threads = newThreads;
				}
			}

			return ImmutableList.copyOf(threads);
		}

		private ImmutableList<PDAStack> tryAdvance(char c) {
			if (stack.isEmpty()) {
				return ImmutableList.of();
			}

			Symbol top = stack.pop();
			checkState(top.isTerminal());

			if (top.terminal() != c) {
				return ImmutableList.of();
			}

			return nonDeterministicallyAdvance();
		}
	}

	private List<PDAStack> stacks;

	private SimplePDA() {
		this.stacks = initStack();
	}

	private static List<PDAStack> initStack() {
		return replaceVariable(Variable.S).stream().map(PDAStack::create).collect(Collectors.toList());
	}

	/**
	 * Recursively replaces the top of the stack with the derivation if it is a variable type.
	 */
	private void advance(char c) {
		List<PDAStack> newStacks = new ArrayList<>();

		for (PDAStack cur : stacks) {
			newStacks.addAll(cur.tryAdvance(c));
		}

		this.stacks = newStacks;
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
		return pda.stacks.stream().anyMatch(PDAStack::isAccepting);
	}
}
