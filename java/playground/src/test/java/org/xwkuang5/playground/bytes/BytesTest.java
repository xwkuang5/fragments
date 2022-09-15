package org.xwkuang5.playground.bytes;

import static com.google.common.truth.Truth.assertThat;

import java.util.Random;
import org.junit.jupiter.api.Test;

public final class BytesTest {

	@Test
	public void findOneByte_smoke() {
		byte one = 0x01;
		assertThat(Bytes.findByte(0x01FFFFFFFFFFFFFFL, one)).isEqualTo(0);
		assertThat(Bytes.findByte(0xFF01FFFFFFFFFFFFL, one)).isEqualTo(1);
		assertThat(Bytes.findByte(0xFFFF01FFFFFFFFFFL, one)).isEqualTo(2);
		assertThat(Bytes.findByte(0xFFFFFF01FFFFFFFFL, one)).isEqualTo(3);
		assertThat(Bytes.findByte(0xFFFFFFFF01FFFFFFL, one)).isEqualTo(4);
		assertThat(Bytes.findByte(0xFFFFFFFFFF01FFFFL, one)).isEqualTo(5);
		assertThat(Bytes.findByte(0xFFFFFFFFFFFF01FFL, one)).isEqualTo(6);
		assertThat(Bytes.findByte(0xFFFFFFFFFFFFFF01L, one)).isEqualTo(7);
	}

	@Test
	public void findZeroByte_smoke() {
		assertThat(Bytes.findZeroByte(0x00FFFFFFFFFFFFFFL)).isEqualTo(0);
		assertThat(Bytes.findZeroByte(0xFF00FFFFFFFFFFFFL)).isEqualTo(1);
		assertThat(Bytes.findZeroByte(0xFFFF00FFFFFFFFFFL)).isEqualTo(2);
		assertThat(Bytes.findZeroByte(0xFFFFFF00FFFFFFFFL)).isEqualTo(3);
		assertThat(Bytes.findZeroByte(0xFFFFFFFF00FFFFFFL)).isEqualTo(4);
		assertThat(Bytes.findZeroByte(0xFFFFFFFFFF00FFFFL)).isEqualTo(5);
		assertThat(Bytes.findZeroByte(0xFFFFFFFFFFFF00FFL)).isEqualTo(6);
		assertThat(Bytes.findZeroByte(0xFFFFFFFFFFFFFF00L)).isEqualTo(7);
	}

	@Test
	public void findByte_compareWithIterative_isSame() {
		var rand = new Random(1);

		for (int i = 0; i < 10; ++i) {
			byte[] singleByte = new byte[1];
			rand.nextBytes(singleByte);
			for (int j = 0; j < 1000000; ++j) {
				long word = rand.nextLong();

				assertThat(Bytes.findByte(word, singleByte[0])).isEqualTo(
						findByteIterative(word, singleByte[0]));
			}
		}
	}

	private static int findByteIterative(long word, byte b) {
		long mask = 0x00000000000000FFL;
		long byteAsLong = Byte.toUnsignedLong(b);
		for (int i = 7; i >= 0; i -= 1) {
			long tmp = word >> (8 * i);
			if ((tmp & mask) == byteAsLong) {
				return 8 - i - 1;
			}
		}
		return 8;
	}
}
