package org.xwkuang5.playground.bytes;

import com.google.auto.value.AutoValue;
import com.google.common.collect.ImmutableList;
import com.google.common.collect.Range;

/**
 * An n-dimensional byte range where each dimension specifies a range of bytes.
 */
@AutoValue
abstract class BytesRange {

	abstract ImmutableList<Range<Byte>> ranges();

	BytesPosition max(BytesPosition position) {
		return position;
	}

	static BytesRange create(ImmutableList<Range<Byte>> ranges) {
		return new AutoValue_BytesRange(ranges);
	}
}
