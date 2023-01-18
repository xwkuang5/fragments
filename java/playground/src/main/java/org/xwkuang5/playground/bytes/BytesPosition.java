package org.xwkuang5.playground.bytes;

import static com.google.common.base.Preconditions.checkArgument;

import com.google.auto.value.AutoValue;
import com.google.protobuf.ByteString;
import java.nio.charset.Charset;

/**
 * Represents a position in the space formed by all arrays of bytes.
 *
 * <p>Supports prefix successor point that represent the location just after all bytes sharing the
 * same prefix.
 */
@AutoValue
abstract class BytesPosition implements Comparable<BytesPosition> {

	abstract boolean isSuffixInfinity();

	abstract ByteString bytes();

	static BytesPosition create(byte[] bytes) {
		checkArgument(bytes.length >= 1);
		return new AutoValue_BytesPosition(/* isSuffixInfinity= */ false, ByteString.copyFrom(bytes));
	}

	static BytesPosition successor(byte[] bytes) {
		checkArgument(bytes.length >= 1);
		return new AutoValue_BytesPosition(/* isSuffixInfinity= */ true, ByteString.copyFrom(bytes));
	}

	@Override
	public int compareTo(BytesPosition other) {
		int size = bytes().size();
		int otherSize = other.bytes().size();
		int minSize = Math.min(size, otherSize);

		int cmp = bytes().substring(0, minSize)
				.toString(Charset.defaultCharset())
				.compareTo(other.bytes().substring(0, minSize).toString(Charset.defaultCharset()));

		if (cmp != 0) {
			return cmp;
		}

		// other is shorter
		if (size > minSize) {
			if (other.isSuffixInfinity()) {
				return -1;
			}
			return 1;
		}

		// *this is shorter
		if (otherSize > minSize) {
			if (isSuffixInfinity()) {
				return 1;
			}
			return -1;
		}

		return isSuffixInfinity()
				? other.isSuffixInfinity() ? 0 : 1
				: other.isSuffixInfinity() ? -1 : 0;
	}
}
