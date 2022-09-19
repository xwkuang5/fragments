package org.xwkuang5.playground.collect;

import static com.google.common.truth.Truth.assertThat;
import static org.junit.Assert.assertThrows;

import org.junit.jupiter.api.Test;

public final class RingBufferTest {

	@Test
	public void construct_zeroLength_throws() {
		assertThrows(IllegalArgumentException.class, () -> new RingBuffer<>(Integer.class, 0));
		assertThrows(IllegalArgumentException.class, () -> new RingBuffer<>(Integer.class, -1));
	}

	@Test
	public void size() {
		var buffer = new RingBuffer<>(Integer.class, 1);

		assertThat(buffer.size()).isEqualTo(0);

		buffer.add(1);
		assertThat(buffer.size()).isEqualTo(1);

		buffer.peek();
		assertThat(buffer.size()).isEqualTo(1);

		buffer.remove();
		assertThat(buffer.size()).isEqualTo(0);
	}

	@Test
	public void add_remove_peek() {
		var buffer = new RingBuffer<>(Integer.class, 3);

		buffer.add(1);
		buffer.add(2);
		buffer.add(3);

		assertThat(buffer.peek()).isEqualTo(1);
		assertThat(buffer.remove()).isEqualTo(1);
		assertThat(buffer.peek()).isEqualTo(2);
		assertThat(buffer.remove()).isEqualTo(2);
		assertThat(buffer.peek()).isEqualTo(3);
		assertThat(buffer.remove()).isEqualTo(3);
	}

	@Test
	public void add_bufferFull_throws() {
		var buffer = new RingBuffer<>(Integer.class, 1);

		buffer.add(1);

		assertThrows(IllegalStateException.class, () -> buffer.add(2));
	}

	@Test
	public void remove_emptyBuffer_throws() {
		var buffer = new RingBuffer<>(Integer.class, 1);

		assertThrows(IllegalStateException.class, buffer::remove);
	}

	@Test
	public void peek_emptyBuffer_throws() {
		var buffer = new RingBuffer<>(Integer.class, 1);

		assertThrows(IllegalStateException.class, buffer::peek);
	}
}
