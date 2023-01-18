package org.xwkuang5.playground.bytes;

import static com.google.common.truth.Truth.assertThat;
import static org.xwkuang5.playground.bytes.BytesPosition.before;
import static org.xwkuang5.playground.bytes.BytesPosition.after;

import com.google.common.collect.ImmutableList;
import com.google.common.collect.Range;
import java.util.ArrayList;
import org.junit.jupiter.api.Test;

final class BytesRangeTest {

	@Test
	public void restrict_closedClosed_closedClosed() {
		var range = BytesRange.create(ImmutableList.of(Range.closed((byte) 0x01, (byte) 0x03),
				Range.closed((byte) 0x01, (byte) 0x03)));

		assertThat(range.max(before(new byte[]{0x01}))).isEqualTo(before(new byte[]{0x01, 0x01}));
		assertThat(range.max(before(new byte[]{0x01, 0x01}))).isEqualTo(before(new byte[]{0x01, 0x01}));
		assertThat(range.max(before(new byte[]{0x01, 0x03}))).isEqualTo(before(new byte[]{0x01, 0x03}));
		assertThat(range.max(before(new byte[]{0x01, 0x04}))).isEqualTo(after(new byte[]{0x01}));
		assertThat(range.max(before(new byte[]{0x03, 0x01}))).isEqualTo(before(new byte[]{0x03, 0x01}));
		assertThat(range.max(before(new byte[]{0x03, 0x03}))).isEqualTo(before(new byte[]{0x03, 0x03}));
		assertThat(range.max(before(new byte[]{0x03, 0x04}))).isEqualTo(after(new byte[]{0x03}));

		assertThat(range.max(after(new byte[]{0x01, 0x00}))).isEqualTo(before(new byte[]{0x01, 0x01}));
		assertThat(range.max(after(new byte[]{0x01, 0x01}))).isEqualTo(after(new byte[]{0x01, 0x01}));
		assertThat(range.max(after(new byte[]{0x01, 0x02}))).isEqualTo(after(new byte[]{0x01, 0x02}));
		assertThat(range.max(after(new byte[]{0x01, 0x03}))).isEqualTo(after(new byte[]{0x01}));
		assertThat(range.max(after(new byte[]{0x02, 0x03}))).isEqualTo(after(new byte[]{0x02}));
		assertThat(range.max(after(new byte[]{0x03, 0x03}))).isEqualTo(after(new byte[]{0x03}));
		assertThat(range.max(after(new byte[]{0x01}))).isEqualTo(after(new byte[]{0x01}));
		assertThat(range.max(after(new byte[]{0x02}))).isEqualTo(after(new byte[]{0x02}));
		assertThat(range.max(after(new byte[]{0x03}))).isEqualTo(after(new byte[]{0x03}));
	}
}
