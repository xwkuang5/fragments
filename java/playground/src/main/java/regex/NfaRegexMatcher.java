package regex;

import static com.google.common.base.Preconditions.checkArgument;
import static com.google.common.base.Preconditions.checkNotNull;
import static com.google.common.base.Preconditions.checkState;

import com.google.auto.value.AutoOneOf;
import com.google.auto.value.AutoValue;
import com.google.common.collect.ImmutableList;
import com.google.common.collect.Iterables;
import java.util.Stack;
import java.util.function.Consumer;
import java.util.stream.Stream;
import org.jspecify.nullness.Nullable;

/**
 * Constructs an NFA-based regex matcher from a reversed polish form regex string.
 *
 * <p>This implementation is derived from <a href="https://swtch.com/~rsc/regexp/regexp1.html">Russ
 * Cox's regex tutorial</a>.
 */
public final class NfaRegexMatcher {

	private final State start;

	private static boolean isSupportedAtom(char ch) {
		return Character.isLetter(ch) || Character.isDigit(ch);
	}

	private static boolean isSupportedSpecialForm(char ch) {
		return ch == '*' || ch == '+' || ch == '?' || ch == '|' || ch == '.';
	}

	@AutoOneOf(State.Type.class)
	abstract static class State {

		static final State END_STATE = State.ofEnd();

		enum Type {
			SPLIT,
			INPUT,
			END
		}

		abstract Type type();

		abstract SplitState split();

		abstract InputState input();

		abstract void end();

		/**
		 * Returns the set of states reachable from the current state.
		 */
		Stream<State> reachable() {
			switch (type()) {
				case SPLIT:
					return Stream.concat(split().top().reachable(), split().bottom().reachable());
				case INPUT:
					// fall through
				case END:
					return Stream.of(this);
			}
			throw new AssertionError("impossible");
		}

		/**
		 * Returns the next state of the current state on {@code ch}.
		 */
		Stream<State> next(char ch) {
			switch (type()) {
				case SPLIT:
					throw new IllegalStateException("unexpected split state");
				case INPUT:
					InputState inputState = input();
					return ch == inputState.input() ? Stream.of(inputState.next()) : Stream.empty();
				case END:
					return Stream.empty();
			}
			throw new AssertionError("impossible");
		}

		static State ofSplit(SplitState split) {
			return AutoOneOf_NfaRegexMatcher_State.split(split);
		}

		static State ofInput(InputState start) {
			return AutoOneOf_NfaRegexMatcher_State.input(start);
		}

		static State ofEnd() {
			return AutoOneOf_NfaRegexMatcher_State.end();
		}
	}

	// TODO(xwkuang5): is java default `equals` the right equality to aim for?
	static class InputState {

		private final char input;
		private @Nullable State next;

		private static InputState of(char input) {
			checkArgument(isSupportedAtom(input));
			return new InputState(input, null);
		}

		private InputState(char input, @Nullable State next) {
			this.input = input;
			this.next = next;
		}

		private void setNext(State next) {
			checkNotNull(next);

			this.next = next;
		}

		private char input() {
			return input;
		}

		private State next() {
			checkNotNull(next);

			return next;
		}
	}

	// TODO(xwkuang5): is java default `equals` the right equality to aim for?
	static class SplitState {

		private @Nullable State top;
		private @Nullable State bottom;

		private SplitState(@Nullable State top, @Nullable State bottom) {
			this.top = top;
			this.bottom = bottom;
		}

		private void setTop(State top) {
			this.top = top;
		}

		private void setBottom(State bottom) {
			this.bottom = bottom;
		}

		private State top() {
			checkNotNull(top);
			return top;
		}

		private State bottom() {
			checkNotNull(bottom);
			return bottom;
		}
	}

	@AutoValue
	abstract static class Fragment {

		abstract State start();

		/**
		 * A list of outstanding wires whose next state remains to be set.
		 */
		abstract ImmutableList<Consumer<State>> fringes();

		private static Fragment from(InputState start) {
			return new AutoValue_NfaRegexMatcher_Fragment(State.ofInput(start), ImmutableList.of(start::setNext));
		}

		private static Fragment create(State start, ImmutableList<Consumer<State>> fringes) {
			return new AutoValue_NfaRegexMatcher_Fragment(start, fringes);
		}
	}

	private static class FragmentStack {

		private final Stack<Fragment> stack;

		FragmentStack(Fragment start) {
			stack = new Stack<>();
			stack.add(start);
		}

		void onZeroOrMore() {
			checkState(!stack.isEmpty());
			Fragment fragment = stack.pop();

			SplitState split = new SplitState(fragment.start(), /* bottom= */ null);
			fragment.fringes().forEach((consumer) -> consumer.accept(State.ofSplit(split)));

			stack.push(Fragment.create(State.ofSplit(split), ImmutableList.of(split::setBottom)));
		}

		void onOneOrMore() {
			checkState(!stack.isEmpty());
			Fragment fragment = stack.pop();

			SplitState split = new SplitState(fragment.start(), /* bottom= */ null);
			fragment.fringes().forEach((consumer) -> consumer.accept(State.ofSplit(split)));

			stack.push(Fragment.create(fragment.start(), ImmutableList.of(split::setBottom)));
		}

		void onZeroOrOne() {
			checkState(!stack.isEmpty());
			Fragment fragment = stack.pop();

			SplitState split = new SplitState(fragment.start(), /* bottom= */ null);

			ImmutableList<Consumer<State>> fringes =
					ImmutableList.<Consumer<State>>builder()
							.addAll(fragment.fringes())
							.add(split::setBottom)
							.build();

			stack.push(Fragment.create(State.ofSplit(split), fringes));
		}

		void onAlternation() {
			checkState(stack.size() >= 2);
			Fragment e2 = stack.pop();
			Fragment e1 = stack.pop();

			SplitState split = new SplitState(e1.start(), e2.start());

			stack.push(
					Fragment.create(
							State.ofSplit(split),
							ImmutableList.copyOf(Iterables.concat(e1.fringes(), e2.fringes()))));
		}

		void onConcatenation() {
			checkState(stack.size() >= 2);
			Fragment e2 = stack.pop();
			Fragment e1 = stack.pop();

			e1.fringes().forEach((consumer) -> consumer.accept(e2.start()));

			stack.push(Fragment.create(e1.start(), e2.fringes()));
		}

		void onAtom(char ch) {
			InputState newState = InputState.of(ch);
			Fragment newFragment =
					Fragment.create(State.ofInput(newState), ImmutableList.of(newState::setNext));
			stack.push(newFragment);
		}

		State finish() {
			Fragment fragment = Iterables.getOnlyElement(stack);
			fragment.fringes().forEach((consumer) -> consumer.accept(State.END_STATE));
			return fragment.start();
		}
	}

	/**
	 * Returns the non-deterministic finite state automata from compiling the {@code regex} pattern.
	 *
	 * <p>Note {@code regex} must be in <a
	 * href="https://en.wikipedia.org/wiki/Reverse_Polish_notation">reverse-polish-notation</a>.
	 * {@code "."} is used for concatenation. The regex wildcard {@code "."} is not supported yet.
	 * Examples:
	 *
	 * <ul>
	 *   <li>{@code "ab."} => {@code "ab"}
	 *   <li>{@code "ab|"} => {@code "a|b"}
	 *   <li>{@code "ab.*"} => {@code "(ab)*"}
	 *   <li>{@code "ab|*"} => {@code "(a|b)*"}
	 * </ul>
	 */
	public static NfaRegexMatcher compile(String regex) {
		if (regex.isEmpty()) {
			return new NfaRegexMatcher(State.END_STATE);
		}

		int index = 0;
		FragmentStack stack = new FragmentStack(Fragment.from(InputState.of(regex.charAt(index++))));

		while (index < regex.length()) {
			char character = regex.charAt(index++);
			checkArgument(isSupportedAtom(character) || isSupportedSpecialForm(character));
			switch (character) {
				case '+':
					stack.onOneOrMore();
					break;
				case '*':
					stack.onZeroOrMore();
					break;
				case '?':
					stack.onZeroOrOne();
					break;
				case '|':
					stack.onAlternation();
					break;
				case '.':
					stack.onConcatenation();
					break;
				default:
					stack.onAtom(character);
					break;
			}
		}

		return new NfaRegexMatcher(stack.finish());
	}

	public boolean match(String input) {
		Stream<State> states = start.reachable();
		for (int i = 0; i < input.length(); i++) {
			char ch = input.charAt(i);
			states = states.flatMap(s -> s.next(ch)).flatMap(State::reachable);
		}
		return states.anyMatch(State.END_STATE::equals);
	}

	private NfaRegexMatcher(State start) {
		this.start = start;
	}
}
