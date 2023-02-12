package org.xwkuang5.playground.planner;

import static com.google.common.base.Preconditions.checkArgument;
import static com.google.common.collect.ImmutableList.toImmutableList;
import static com.google.common.collect.ImmutableSet.toImmutableSet;

import com.google.auto.value.AutoOneOf;
import com.google.common.collect.ImmutableList;
import com.google.common.collect.ImmutableSet;
import com.google.common.collect.Sets;
import java.util.Set;

/**
 * Representation of boolean predicate
 *
 * <p>Supports converting an arbitrary boolean predicate into conjunctive normal form or
 * disjunctive normal form.</p>
 */
@AutoOneOf(Predicate.Type.class)
abstract class Predicate {

	enum Type {
		NOT, AND, OR, LITERAL
	}

	abstract Type type();

	abstract Predicate not();

	abstract ImmutableSet<Predicate> and();

	abstract ImmutableSet<Predicate> or();

	abstract String literal();

	static Predicate not(Predicate predicate) {

		return AutoOneOf_Predicate.not(predicate);
	}

	static Predicate and(Set<Predicate> predicates) {
		checkArgument(!predicates.isEmpty());

		return AutoOneOf_Predicate.and(ImmutableSet.copyOf(predicates));
	}

	static Predicate and(Predicate a, Predicate... others) {
		return and(ImmutableSet.<Predicate>builder()
				.add(a)
				.addAll(ImmutableSet.copyOf(others)).build());
	}

	static Predicate or(Set<Predicate> predicates) {
		checkArgument(!predicates.isEmpty());

		return AutoOneOf_Predicate.or(ImmutableSet.copyOf(predicates));
	}

	static Predicate or(Predicate a, Predicate... others) {
		return or(ImmutableSet.<Predicate>builder()
				.add(a)
				.addAll(ImmutableSet.copyOf(others)).build());
	}

	static Predicate literal(String literal) {
		checkArgument(!literal.isEmpty());

		return AutoOneOf_Predicate.literal(literal);
	}

	Predicate toDnf() {
		switch (type()) {
			case LITERAL:
				return or(ImmutableSet.of(and(ImmutableSet.of(this))));
			case NOT:
				return or(not().toCnf().and().stream().map(Predicate::negate).collect(toImmutableSet()));
			case AND:
				var cnf = toCnf();
				ImmutableList<ImmutableSet<Predicate>> conjunctions = cnf.and().stream().map(p -> p.or())
						.collect(toImmutableList());
				return or(Sets.cartesianProduct(conjunctions).stream().map(ImmutableSet::copyOf)
						.map(Predicate::and).collect(toImmutableSet()));
			case OR:
				return or(or().stream().flatMap(disjunction -> disjunction.toDnf().or().stream())
						.collect(toImmutableSet()));
		}
		throw new AssertionError("impossible");
	}

	Predicate toCnf() {
		switch (type()) {
			case LITERAL:
				return and(ImmutableSet.of(or(ImmutableSet.of(this))));
			case NOT: {
				return and(not().toDnf().or().stream().map(Predicate::negate).collect(toImmutableSet()));
			}
			case AND:
				return and(and().stream().flatMap(conjunction -> conjunction.toCnf().and().stream())
						.collect(toImmutableSet()));
			case OR:
				var dnf = toDnf();
				ImmutableList<ImmutableSet<Predicate>> disjunctions = dnf.or().stream().map(p -> p.and())
						.collect(toImmutableList());

				return and(Sets.cartesianProduct(disjunctions)
						.stream()
						.map(ImmutableSet::copyOf)
						.map(Predicate::or)
						.collect(toImmutableSet()));
		}
		throw new AssertionError("impossible");
	}

	/**
	 * Converts the sub-predicate into negation normal form by applying the de morgan's law.
	 */
	private Predicate negate() {
		return switch (type()) {
			case LITERAL -> not(this);
			case NOT -> not();
			case AND -> or(and().stream().map(Predicate::negate).collect(toImmutableSet()));
			case OR -> and(or().stream().map(Predicate::negate).collect(toImmutableSet()));
		};
	}
}
