#include "lsolve.h"
#include "version.h"
{% if model.c_only %}
#include "code.h"
#include <stdlib.h>
{% else %}
#include "model.h"
{% endif %}
#include <stdio.h>
#include <math.h>

void initialEquations(CBD* cbd) {
	Real delta = 0.0001;
	{% for eq in equations0 %}
		{% if eq is string %}
	{{ eq }};
		{% else %}

	// Algebraic Loop
	Real _C{{ loop.index0 }}[{{eq[0]|length}}][{{eq[0]|length + 1}}] = {{ eq[1] }};
	agloop(&_C{{ loop.index0 }}, {{eq|length}}{% for block in eq[0] %}, &_{{ block }}{% endfor %});

		{% endif %}
	{% endfor %}

	cbd->time_last = cbd->time;
}

void calculateEquations(CBD* cbd) {
	Real delta = cbd->time - cbd->time_last;

	{% for eq in equations %}
		{% if eq is string %}
	{{ eq }};
		{% else %}

	// Algebraic Loop
	Real _C{{ loop.index0 }}[{{eq[0]|length}}][{{eq[0]|length + 1}}] = {{ eq[1] }};
	agloop(&_C{{ loop.index0 }}, {{eq|length}}{% for block in eq[0] %}, &_{{ block }}{% endfor %});

		{% endif %}
	{% endfor %}

	cbd->time_last = cbd->time;
}

void getContinuousStates(CBD* cbd, double x[], size_t nx) {
	{% for var in derivatives %}
	x[{{ loop.index0 }}] = _{{ var.name }};
	{% endfor %}
}

void setContinuousStates(CBD* cbd, const double x[], size_t nx) {
	{% for var in derivatives %}
	_{{ var.name }} = x[{{ loop.index0 }}];
	{% endfor %}
//	calculateEquations(cbd);
}

void getDerivatives(CBD* cbd, double dx[], size_t nx) {
	{% for der in derivatives %}
		{% set idx = loop.index0 %}
		{% for var in variables %}
			{% if var.index == der.derivative %}
	dx[{{ idx }}] = _{{ var.name }};
			{% endif %}
		{% endfor %}
	{% endfor %}
//	calculateEquations(cbd);
}

void getStateEvents(CBD* cbd, double z[], size_t nz) {
	// No state events found
}

void stateEvent(CBD* cbd) {
	// No state events found
	cbd->nominalsOfContinuousStatesChanged = False;
	cbd->terminateSimulation = False;
	cbd->nextEventTimeDefined = False;
}

Status doStep(CBD* cbd, double t, double tNext) {
	// No state events found
	Boolean timeEvent;

	{% set num_states = derivatives|length %}
	{% if num_states > 0 %}
	double x[{{ num_states }}] = { 0 };
	double dx[{{ num_states }}] = { 0 };
	{% endif %}

	double h = tNext - t;
	while(cbd->time + h < tNext + 0.01 * h) {
		{% if num_states > 0 %}
		getContinuousStates(cbd, x, {{ num_states }});
		getDerivatives(cbd, dx, {{ num_states }});

		// Forward Euler
		for(int i = 0; i < {{ num_states }}; ++i) {
			x[i] += h * dx[i];
		}

		setContinuousStates(cbd, x, {{ num_states }});
		{% endif %}

		timeEvent = cbd->nextEventTimeDefined && cbd->time >= cbd->nextEventTime;

		if(timeEvent) {
			stateEvent(cbd);
		}

		if(cbd->terminateSimulation) {
			// Force termination
			return Discard;
		}
		cbd->time += h;
		calculateEquations(cbd);
	}

	return OK;
}

{% if model.c_only %}
/* SIMULATOR */
int main(int argc, char *args[]) {
	CBD* cbd = (CBD*)malloc(sizeof(CBD));
	cbd->time = {{ model.experiment.start }};
	cbd->time_last = {{ model.experiment.start }};
	cbd->terminateSimulation = 0;
	cbd->nominalsOfContinuousStatesChanged = 0;
	cbd->nextEventTimeDefined = 0;
	cbd->nextEventTime = 0;

	double delta = {{ model.experiment.delta }};

	initialEquations(cbd);
	cbd->time += delta;
	for(int j = 0; j < M; ++j) {
		cbd->history[0][j] = cbd->signals[j];
	}

	for(int i = 1; i < N; ++i) {
		double res = doStep(cbd, cbd->time, cbd->time + delta);
		if(res == Discard) {
			break;
		}
		calculateEquations(cbd);
		for(int j = 0; j < M; ++j) {
			cbd->history[i][j] = cbd->signals[j];
		}
	}

	printf("\t%-20s = %12.4f\n", "TIME", cbd->time);
	{% for var in variables %}
		{% if var.visible %}
	printf("\t%-20s = %12.4f\n", "{{ var.path }}", _{{ var.name }});
		{% endif %}
	{% endfor %}
}
{% endif %}
