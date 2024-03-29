//
// Academic License - for use in teaching, academic research, and meeting
// course requirements at degree granting institutions only.  Not for
// government, commercial, or other organizational use.
// File: envelope.h
//
// MATLAB Coder version            : 5.0
// C/C++ source code generated on  : 07-May-2021 23:24:34
//
#ifndef ENVELOPE_H
#define ENVELOPE_H

// Include Files
#include <cstddef>
#include <cstdlib>
#include "rtwtypes.h"
#include "getPeaksGlobal_types.h"

// Function Declarations
extern void b_envelope(const double x[529200], double n, double upperEnv[529200],
  double lowerEnv[529200]);
extern void envelope(const double x[44100], double n, double upperEnv[44100],
                     double lowerEnv[44100]);

#endif

//
// File trailer for envelope.h
//
// [EOF]
//
