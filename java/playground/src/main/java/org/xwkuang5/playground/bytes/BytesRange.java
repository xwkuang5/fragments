package org.xwkuang5.playground.bytes;

import static com.google.common.base.Preconditions.checkArgument;
import static com.google.common.base.Preconditions.checkState;
import static java.lang.Math.max;

import com.google.auto.value.AutoValue;
import com.google.common.collect.BoundType;
import com.google.common.collect.ImmutableList;
import com.google.common.collect.Range;
import com.google.protobuf.ByteString;
import java.nio.ByteBuffer;

/**
 * An n-dimensional byte range where each dimension specifies a range of bytes.
 */
@AutoValue
abstract class BytesRange {

	abstract ImmutableList<Range<Byte>> ranges();

	BytesPosition clip(BytesPosition position) {

		ByteBuffer bb = ByteBuffer.allocate(max(ranges().size(), position.bytes().size()));

		var rangeIter = ranges().iterator();
		var bytesIter = position.bytes().iterator();

		boolean byteSmallerThanMin = false;
		boolean byteLargerThanMax = false;

		while (rangeIter.hasNext() && bytesIter.hasNext()) {
			byte curByte = bytesIter.nextByte();
			var range = rangeIter.next();

			if (range.contains(curByte)) {
				bb.put(curByte);
			} else {
				if (range.lowerEndpoint() >= curByte) {
					byteSmallerThanMin = true;
					break;
				} else if (range.upperEndpoint() <= curByte) {
					byteLargerThanMax = true;
					break;
				}
				throw new AssertionError("impossible");
			}
		}

		if (byteSmallerThanMin) {
			var prefix = ByteString.copyFrom(bb.array(), bb.arrayOffset(), bb.position());
			var postfix = longestInclusiveLowerBound(prefix.size());
			if (postfix.isEmpty()) {
				var nextRange = ranges().get(prefix.size());
				checkState(nextRange.lowerBoundType().equals(BoundType.OPEN));
				return BytesPosition.after(
						prefix.concat(ByteString.copyFrom(new byte[]{nextRange.lowerEndpoint()})));
			}
			return BytesPosition.before(prefix.concat(postfix));
		}

		if (byteLargerThanMax) {
			if (bb.position() == 0) {
				return position;
			}
			return BytesPosition.after(ByteString.copyFrom(bb.array(), bb.arrayOffset(), bb.position()));
		}

		if (!rangeIter.hasNext()) {
			return position;
		}

		// position is a prefix of the range
		if (!bytesIter.hasNext()) {
			if (position.isSuffixInfinity()) {
				return BytesPosition.after(
						ByteString.copyFrom(bb.array(), bb.arrayOffset(), bb.position()));
			} else {
				var prefix = ByteString.copyFrom(bb.array(), bb.arrayOffset(), bb.position());
				var postfix = longestInclusiveLowerBound(prefix.size());
				if (postfix.isEmpty()) {
					var nextRange = ranges().get(prefix.size());
					checkState(nextRange.lowerBoundType().equals(BoundType.OPEN));
					return BytesPosition.after(
							prefix.concat(ByteString.copyFrom(new byte[]{nextRange.lowerEndpoint()})));
				}
				return BytesPosition.before(prefix.concat(postfix));
			}
		}

		throw new AssertionError("impossible");
	}

	ByteString longestInclusiveLowerBound(int from) {
		if (from == ranges().size()) {
			return ByteString.EMPTY;
		}
		ByteBuffer bb = ByteBuffer.allocate(ranges().size() - from);
		for (int i = from; i < ranges().size(); ++i) {
			if (ranges().get(i).lowerBoundType().equals(BoundType.CLOSED)) {
				bb.put(ranges().get(i).lowerEndpoint());
				continue;
			}
			break;
		}
		return ByteString.copyFrom(bb.array(), bb.arrayOffset(), bb.position());
	}

	static BytesRange create(ImmutableList<Range<Byte>> ranges) {
		ranges.forEach(r -> checkArgument(!r.isEmpty(), "range can not be empty"));
		return new AutoValue_BytesRange(ranges);
	}
}
