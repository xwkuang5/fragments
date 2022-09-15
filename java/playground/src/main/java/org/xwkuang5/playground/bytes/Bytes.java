package org.xwkuang5.playground.bytes;

public class Bytes {

	public static int findZeroByte(long word) {
		// tmp is 0x7F iff word is 0x00 or 0x80. All other values of word have the 8th bit in a byte set to 1.
		long tmp = (word & 0x7F7F7F7F7F7F7F7FL) + 0x7F7F7F7F7F7F7F7FL;
		// tmp is 0x7F iff word is 0x00 or 0x80. All other values of word become 0xFF.
		tmp = tmp | 0x7F7F7F7F7F7F7F7FL;
		// tmp is 0x7F iff word is 0x00. All other values of word become 0xFF.
		tmp = word | tmp;
		// tmp is non-zero iff word is 0x00.
		tmp = ~tmp;
		// divide by 8 to find the byte position.
		return Long.numberOfLeadingZeros(tmp) >>> 3;
	}

	public static int findByte(long word, byte b) {
		if (b == 0x00) {
			return findZeroByte(word);
		}
		long byteAsLong = Byte.toUnsignedLong(b);
		long tiledByte =
				byteAsLong << 56 | byteAsLong << 48 | byteAsLong << 40 | byteAsLong << 32 | byteAsLong << 24
						| byteAsLong << 16 | byteAsLong << 8 | byteAsLong;
		long tmp = word ^ tiledByte;
		return findZeroByte(tmp);
	}
}
