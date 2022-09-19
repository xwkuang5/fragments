package org.xwkuang5.playground.collect;

import static com.google.common.base.Preconditions.checkArgument;
import static com.google.common.base.Preconditions.checkState;

import java.lang.reflect.Array;

public final class RingBuffer<T> {

	private final T[] buffer;
	private final int length;
	private int count;
	private int start;
	private int end;

	public RingBuffer(Class<T> clazz, int capacity) {
		checkArgument(capacity >= 1);

		this.buffer = (T[]) Array.newInstance(clazz, capacity);
		this.length = capacity;
		this.count = 0;
		this.start = 0;
		this.end = 0;
	}

	public int size() {
		return count;
	}

	public void add(T o) {
		checkState(count < length);
		buffer[end] = o;
		end = (end + 1) % length;
		count += 1;
	}

	public T remove() {
		checkState(count >= 1);
		T ret = buffer[start];
		start = (start + 1) % length;
		count -= 1;
		return ret;
	}

	public T peek() {
		checkState(count >= 1);
		return buffer[start];
	}
}
