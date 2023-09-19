package org.xwkuang5.playground.parse;

import static org.xwkuang5.playground.parse.SimplePDA.match;

import static com.google.common.truth.Truth.assertThat;

import org.junit.jupiter.api.Test;

final class SimplePDATest {

	@Test
	public void match_isMatch_returnsTrue() {
		assertThat(match("")).isTrue();
		assertThat(match("01")).isTrue();
		assertThat(match("0011")).isTrue();
		assertThat(match("000111")).isTrue();
	}

	@Test
	public void match_isNotMatch_returnsFalse() {
		assertThat(match("0")).isFalse();
		assertThat(match("00")).isFalse();
		assertThat(match("11")).isFalse();
		assertThat(match("000")).isFalse();
		assertThat(match("001")).isFalse();
		assertThat(match("010")).isFalse();
		assertThat(match("011")).isFalse();
		assertThat(match("100")).isFalse();
		assertThat(match("101")).isFalse();
		assertThat(match("110")).isFalse();
		assertThat(match("111")).isFalse();
	}
}
