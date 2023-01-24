package org.xwkuang5.playground.bytes;

import static com.google.common.truth.Truth.assertThat;
import static org.xwkuang5.playground.bytes.BytesPosition.before;
import static org.xwkuang5.playground.bytes.BytesPosition.after;

import com.google.common.collect.ImmutableList;
import com.google.common.collect.Range;
import org.junit.jupiter.api.Test;

final class BytesRangeTest {

	@Test
	public void restrict_singleRange_closed() {
		var range = BytesRange.create(ImmutableList.of(Range.closed((byte) 0x01, (byte) 0x03)));

		assertThat(range.clip(before(new byte[]{0x00}))).isEqualTo(before(new byte[]{0x01}));
		assertThat(range.clip(before(new byte[]{0x01}))).isEqualTo(before(new byte[]{0x01}));
		assertThat(range.clip(before(new byte[]{0x01, 0x01}))).isEqualTo(
				before(new byte[]{0x01, 0x01}));
		assertThat(range.clip(before(new byte[]{0x02}))).isEqualTo(before(new byte[]{0x02}));
		assertThat(range.clip(before(new byte[]{0x03}))).isEqualTo(before(new byte[]{0x03}));
		assertThat(range.clip(before(new byte[]{0x03, 0x01}))).isEqualTo(
				before(new byte[]{0x03, 0x01}));
		assertThat(range.clip(before(new byte[]{0x04}))).isEqualTo(before(new byte[]{0x04}));

		assertThat(range.clip(after(new byte[]{0x00}))).isEqualTo(before(new byte[]{0x01}));
		assertThat(range.clip(after(new byte[]{0x01}))).isEqualTo(after(new byte[]{0x01}));
		assertThat(range.clip(after(new byte[]{0x01, 0x01}))).isEqualTo(after(new byte[]{0x01, 0x01}));
		assertThat(range.clip(after(new byte[]{0x03}))).isEqualTo(after(new byte[]{0x03}));
	}

	@Test
	public void restrict_singleRange_open() {
		var range = BytesRange.create(ImmutableList.of(Range.open((byte) 0x01, (byte) 0x03)));

		assertThat(range.clip(before(new byte[]{0x00}))).isEqualTo(after(new byte[]{0x01}));
		assertThat(range.clip(before(new byte[]{0x01}))).isEqualTo(after(new byte[]{0x01}));
		assertThat(range.clip(before(new byte[]{0x01, 0x01}))).isEqualTo(after(new byte[]{0x01}));
		assertThat(range.clip(before(new byte[]{0x02}))).isEqualTo(before(new byte[]{0x02}));
		assertThat(range.clip(before(new byte[]{0x03}))).isEqualTo(before(new byte[]{0x03}));
		assertThat(range.clip(before(new byte[]{0x03, 0x01}))).isEqualTo(
				before(new byte[]{0x03, 0x01}));
		assertThat(range.clip(before(new byte[]{0x04}))).isEqualTo(before(new byte[]{0x04}));

		assertThat(range.clip(after(new byte[]{0x00}))).isEqualTo(after(new byte[]{0x01}));
		assertThat(range.clip(after(new byte[]{0x01}))).isEqualTo(after(new byte[]{0x01}));
		assertThat(range.clip(after(new byte[]{0x01, 0x01}))).isEqualTo(after(new byte[]{0x01}));
		assertThat(range.clip(after(new byte[]{0x03}))).isEqualTo(after(new byte[]{0x03}));
	}

	@Test
	public void restrict_closed_closed() {
		var range = BytesRange.create(ImmutableList.of(Range.closed((byte) 0x01, (byte) 0x03),
				Range.closed((byte) 0x01, (byte) 0x03)));

		assertThat(range.clip(before(new byte[]{0x01}))).isEqualTo(before(new byte[]{0x01, 0x01}));
		assertThat(range.clip(before(new byte[]{0x01, 0x01}))).isEqualTo(
				before(new byte[]{0x01, 0x01}));
		assertThat(range.clip(before(new byte[]{0x01, 0x03}))).isEqualTo(
				before(new byte[]{0x01, 0x03}));
		assertThat(range.clip(before(new byte[]{0x01, 0x04}))).isEqualTo(after(new byte[]{0x01}));
		assertThat(range.clip(before(new byte[]{0x03, 0x01}))).isEqualTo(
				before(new byte[]{0x03, 0x01}));
		assertThat(range.clip(before(new byte[]{0x03, 0x03}))).isEqualTo(
				before(new byte[]{0x03, 0x03}));
		assertThat(range.clip(before(new byte[]{0x03, 0x04}))).isEqualTo(after(new byte[]{0x03}));

		assertThat(range.clip(after(new byte[]{0x01, 0x00}))).isEqualTo(before(new byte[]{0x01, 0x01}));
		assertThat(range.clip(after(new byte[]{0x01, 0x01}))).isEqualTo(after(new byte[]{0x01, 0x01}));
		assertThat(range.clip(after(new byte[]{0x01, 0x02}))).isEqualTo(after(new byte[]{0x01, 0x02}));
		assertThat(range.clip(after(new byte[]{0x01, 0x03}))).isEqualTo(after(new byte[]{0x01, 0x03}));
		assertThat(range.clip(after(new byte[]{0x01, 0x03, 0x01}))).isEqualTo(
				after(new byte[]{0x01, 0x03, 0x01}));
		assertThat(range.clip(after(new byte[]{0x01, 0x04}))).isEqualTo(after(new byte[]{0x01}));
		assertThat(range.clip(after(new byte[]{0x02, 0x03}))).isEqualTo(after(new byte[]{0x02, 0x03}));
		assertThat(range.clip(after(new byte[]{0x03, 0x03}))).isEqualTo(after(new byte[]{0x03, 0x03}));
		assertThat(range.clip(after(new byte[]{0x01}))).isEqualTo(after(new byte[]{0x01}));
		assertThat(range.clip(after(new byte[]{0x02}))).isEqualTo(after(new byte[]{0x02}));
		assertThat(range.clip(after(new byte[]{0x03}))).isEqualTo(after(new byte[]{0x03}));
	}

	@Test
	public void restrict_open_open() {
		var range = BytesRange.create(ImmutableList.of(Range.open((byte) 0x01, (byte) 0x03),
				Range.open((byte) 0x01, (byte) 0x03)));

		assertThat(range.clip(before(new byte[]{0x01}))).isEqualTo(after(new byte[]{0x01}));
		assertThat(range.clip(before(new byte[]{0x01, 0x01}))).isEqualTo(after(new byte[]{0x01}));
		assertThat(range.clip(before(new byte[]{0x02}))).isEqualTo(after(new byte[]{0x02, 0x01}));
		assertThat(range.clip(before(new byte[]{0x02, 0x01}))).isEqualTo(after(new byte[]{0x02, 0x01}));
		assertThat(range.clip(before(new byte[]{0x02, 0x02}))).isEqualTo(
				before(new byte[]{0x02, 0x02}));
		assertThat(range.clip(before(new byte[]{0x02, 0x03}))).isEqualTo(after(new byte[]{0x02}));

		assertThat(range.clip(after(new byte[]{0x01}))).isEqualTo(after(new byte[]{0x01}));
		assertThat(range.clip(after(new byte[]{0x01, 0x01}))).isEqualTo(after(new byte[]{0x01}));
		assertThat(range.clip(before(new byte[]{0x02}))).isEqualTo(after(new byte[]{0x02, 0x01}));
		assertThat(range.clip(before(new byte[]{0x02, 0x01}))).isEqualTo(after(new byte[]{0x02, 0x01}));
		assertThat(range.clip(before(new byte[]{0x02, 0x02}))).isEqualTo(
				before(new byte[]{0x02, 0x02}));
		assertThat(range.clip(before(new byte[]{0x02, 0x03}))).isEqualTo(after(new byte[]{0x02}));
		assertThat(range.clip(before(new byte[]{0x03}))).isEqualTo(before(new byte[]{0x03}));
		assertThat(range.clip(before(new byte[]{0x03, 0x01}))).isEqualTo(
				before(new byte[]{0x03, 0x01}));
	}

	@Test
	public void restrict_openClosed_closedOpen() {
		var range = BytesRange.create(ImmutableList.of(Range.openClosed((byte) 0x01, (byte) 0x03),
				Range.closedOpen((byte) 0x01, (byte) 0x03)));

		assertThat(range.clip(before(new byte[]{0x01}))).isEqualTo(after(new byte[]{0x01}));
		assertThat(range.clip(before(new byte[]{0x01, 0x01}))).isEqualTo(after(new byte[]{0x01}));
		assertThat(range.clip(before(new byte[]{0x02}))).isEqualTo(before(new byte[]{0x02, 0x01}));
		assertThat(range.clip(before(new byte[]{0x02, 0x01}))).isEqualTo(
				before(new byte[]{0x02, 0x01}));
		assertThat(range.clip(before(new byte[]{0x02, 0x02}))).isEqualTo(
				before(new byte[]{0x02, 0x02}));
		assertThat(range.clip(before(new byte[]{0x02, 0x03}))).isEqualTo(after(new byte[]{0x02}));

		assertThat(range.clip(after(new byte[]{0x01}))).isEqualTo(after(new byte[]{0x01}));
		assertThat(range.clip(after(new byte[]{0x01, 0x01}))).isEqualTo(after(new byte[]{0x01}));
		assertThat(range.clip(after(new byte[]{0x02}))).isEqualTo(after(new byte[]{0x02}));
		assertThat(range.clip(after(new byte[]{0x02, 0x00}))).isEqualTo(before(new byte[]{0x02, 0x01}));
		assertThat(range.clip(after(new byte[]{0x02, 0x01}))).isEqualTo(after(new byte[]{0x02, 0x01}));
	}
}
