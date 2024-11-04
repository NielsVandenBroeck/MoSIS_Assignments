/*
 *  Main model file; contains the generated CBD model.
 */
#include "fmi2TypesPlatform.h"
#include <stddef.h>

{% set itcnt = ((model.experiment.end - model.experiment.start) / model.experiment.delta)|int %}

#define M {{ variables|length }}     /* No of Variables */
#define N {{ itcnt }}     /* No of Iterations */

typedef int Status;
#define fmi2OK 0
#define fmi2Discard 1
#define fmi2Error 2

// Variable References in-memory
{% for var in variables %}
#define _{{ var.name }} (cbd->signals[{{ loop.index0 }}])
{% endfor %}

typedef struct {
	double time;
	double time_last;

	// event info
	Boolean terminateSimulation;
	Boolean nominalsOfContinuousStatesChanged;
	Boolean nextEventTimeDefined;
	Real nextEventTime;

	double signals[M];
	double history[N][M];
} CBD;

void initialEquations(CBD* cbd);
void calculateEquations(CBD* cbd);

Status doStep(CBD* cbd, double t, double tNext);

void stateEvent(CBD* cbd);
void getContinuousStates(CBD* cbd, double x[], size_t nx);
void setContinuousStates(CBD* cbd, const double x[], size_t nx);
void getDerivatives(CBD* cbd, double dx[], size_t nx);
void getStateEvents(CBD* cbd, double z[], size_t nz);
