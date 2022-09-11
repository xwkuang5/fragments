package org.xwkuang5.playground.regex;

import static com.google.common.truth.Truth.assertThat;

import org.junit.jupiter.api.Test;
import org.xwkuang5.playground.regex.NfaRegexMatcher;

public final class NfaRegexMatcherTest {

	@Test
	public void emptyPattern() {
		NfaRegexMatcher nfa = NfaRegexMatcher.compile("");

		assertThat(nfa.match("")).isTrue();
		assertThat(nfa.match("a")).isFalse();
	}

	@Test
	public void concatenation() {
		NfaRegexMatcher nfa = NfaRegexMatcher.compile("ab.");

		assertThat(nfa.match("ab")).isTrue();
		assertThat(nfa.match("")).isFalse();
		assertThat(nfa.match("a")).isFalse();
		assertThat(nfa.match("b")).isFalse();
		assertThat(nfa.match("aa")).isFalse();
		assertThat(nfa.match("abb")).isFalse();
	}

	@Test
	public void alternation() {
		NfaRegexMatcher nfa = NfaRegexMatcher.compile("ab|");

		assertThat(nfa.match("a")).isTrue();
		assertThat(nfa.match("b")).isTrue();
		assertThat(nfa.match("")).isFalse();
		assertThat(nfa.match("c")).isFalse();
		assertThat(nfa.match("aa")).isFalse();
		assertThat(nfa.match("bb")).isFalse();
	}

	@Test
	public void zeroOrOne() {
		NfaRegexMatcher nfa = NfaRegexMatcher.compile("a?");

		assertThat(nfa.match("a")).isTrue();
		assertThat(nfa.match("")).isTrue();
		assertThat(nfa.match("b")).isFalse();
		assertThat(nfa.match("aa")).isFalse();
	}

	@Test
	public void oneOrMore() {
		NfaRegexMatcher nfa = NfaRegexMatcher.compile("a+");

		assertThat(nfa.match("a")).isTrue();
		assertThat(nfa.match("aa")).isTrue();
		assertThat(nfa.match("aaa")).isTrue();
		assertThat(nfa.match("aaaa")).isTrue();
		assertThat(nfa.match("aaaaa")).isTrue();
		assertThat(nfa.match("")).isFalse();
		assertThat(nfa.match("b")).isFalse();
	}

	@Test
	public void zeroOrMore() {
		NfaRegexMatcher nfa = NfaRegexMatcher.compile("a*");

		assertThat(nfa.match("")).isTrue();
		assertThat(nfa.match("a")).isTrue();
		assertThat(nfa.match("aa")).isTrue();
		assertThat(nfa.match("aaa")).isTrue();
		assertThat(nfa.match("aaaa")).isTrue();
		assertThat(nfa.match("aaaaa")).isTrue();
		assertThat(nfa.match("b")).isFalse();
		assertThat(nfa.match("bb")).isFalse();
	}

	@Test
	public void composite_concatenation_oneOrMore() {
		NfaRegexMatcher nfa = NfaRegexMatcher.compile("ab.+");

		assertThat(nfa.match("ab")).isTrue();
		assertThat(nfa.match("abab")).isTrue();
		assertThat(nfa.match("ababab")).isTrue();
		assertThat(nfa.match("abababab")).isTrue();
		assertThat(nfa.match("")).isFalse();
		assertThat(nfa.match("aa")).isFalse();
		assertThat(nfa.match("bb")).isFalse();
	}

	@Test
	public void composite_concatenation_alternation_oneOrMore() {
		NfaRegexMatcher nfa = NfaRegexMatcher.compile("ab.cd.|+");

		assertThat(nfa.match("ab")).isTrue();
		assertThat(nfa.match("cd")).isTrue();
		assertThat(nfa.match("abab")).isTrue();
		assertThat(nfa.match("abcd")).isTrue();
		assertThat(nfa.match("cdab")).isTrue();
		assertThat(nfa.match("ababab")).isTrue();
		assertThat(nfa.match("abcdab")).isTrue();
		assertThat(nfa.match("")).isFalse();
		assertThat(nfa.match("aa")).isFalse();
		assertThat(nfa.match("bb")).isFalse();
	}

	@Test
	public void composite_concatenation_alternation_zeroOrMore() {
		NfaRegexMatcher nfa = NfaRegexMatcher.compile("ab.cd.|*");

		assertThat(nfa.match("")).isTrue();
		assertThat(nfa.match("ab")).isTrue();
		assertThat(nfa.match("cd")).isTrue();
		assertThat(nfa.match("abab")).isTrue();
		assertThat(nfa.match("abcd")).isTrue();
		assertThat(nfa.match("cdab")).isTrue();
		assertThat(nfa.match("ababab")).isTrue();
		assertThat(nfa.match("abcdab")).isTrue();
		assertThat(nfa.match("aa")).isFalse();
		assertThat(nfa.match("bb")).isFalse();
	}
}
