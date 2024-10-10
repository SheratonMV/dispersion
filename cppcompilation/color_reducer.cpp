/*
 * CIEDE2000.cpp
 * Part of http://github.com/gfiumara/CIEDE2000 by Gregory Fiumara.
 * See LICENSE for details.
 */
#define DllExport   __declspec( dllexport )
#include <cmath>
#include <iostream>
#include <omp.h>
using namespace std;
//#include <CIEDE2000.h>


#ifdef _MSC_VER
#define DLL_EXPORT  __declspec( dllexport )
#else
#define DLL_EXPORT
#endif



/*******************************************************************************
 * Conversions.
 ******************************************************************************/
//extern "C" double CIEDE2000( double, double,double, double,double, double);
constexpr double deg2Rad(const double deg)
{
	return (deg * (3.1415 / 180.0));
}

constexpr double rad2Deg(const double rad)
{
	return ((180.0 / 3.1415) * rad);
}

#ifdef __cplusplus
extern "C"{
#endif

DLL_EXPORT int *simplecolors(double *l1arr, double *a1arr,double *b1arr, double *l2arr, double *a2arr,double *b2arr, int *retpos, const int an,const int bn)
{
	/*
	 * "For these and all other numerical/graphical 􏰀delta E00 values
	 * reported in this article, we set the parametric weighting factors
	 * to unity(i.e., k_L = k_C = k_H = 1.0)." (Page 27).
	 */
    const double k_L = 1.0, k_C = 1.0, k_H = 1.0;
	const double deg360InRad = deg2Rad(360.0);
	const double deg180InRad = deg2Rad(180.0);
	const double pow25To7 = 6103515625.0;
	double tempmaxe, l1, a1, b1, l2, a2, b2, C1, C2, barC, G, a1Prime, a2Prime, CPrime1, CPrime2, hPrime1, hPrime2, deltaLPrime, deltaHPrime, deltahPrime, deltaCPrime, CPrimeProduct, barCPrime, barhPrime, barLPrime, hPrimeSum, T, deltaE, deltaTheta, R_C, S_C, S_H, S_L, R_T;
    int ini, oi, tempmaxpos, indfind, indfindind;
    #pragma omp parallel for shared(retpos), private(ini, indfind, indfindind, tempmaxe, tempmaxpos, l1, a1, b1, l2, a2, b2, C1, C2, barC, G, a1Prime, a2Prime, CPrime1, CPrime2, hPrime1, hPrime2, deltaLPrime, deltaHPrime, deltahPrime, deltaCPrime, CPrimeProduct, barCPrime, barhPrime, barLPrime, hPrimeSum, T, deltaE, deltaTheta, R_C, S_C, S_H, S_L, R_T)
    for (oi =0; oi<an; oi++)
    {
    deltaE=0.0;
    tempmaxe = 10000.0;
    tempmaxpos = 0;

    for (ini =0; ini<bn; ini++)
    {
     l1 = l1arr[oi];
	 a1 = a1arr[oi];
	 b1 = b1arr[oi];
	 l2 = l2arr[ini];
	 a2 = a2arr[ini];
	 b2 = b2arr[ini];
	 /* pow(25, 7) */

	/*
	 * Step 1
	 */
	/* Equation 2 */
	C1 = sqrt((a1 * a1) + (b1 * b1));
	C2 = sqrt((a2 * a2) + (b2 * b2));
	/* Equation 3 */
	 barC = (C1 + C2) / 2.0;
	/* Equation 4 */
	 G = 0.5 * (1 - sqrt(pow(barC, 7) / (pow(barC, 7) + pow25To7)));
	/* Equation 5 */
	a1Prime = (1.0 + G) * a1;
	a2Prime = (1.0 + G) * a2;
	/* Equation 6 */
	CPrime1 = sqrt((a1Prime * a1Prime) + (b1 * b1));
	CPrime2 = sqrt((a2Prime * a2Prime) + (b2 * b2));
	/* Equation 7 */
	if (b1 == 0 && a1Prime == 0)
		hPrime1 = 0.0;
	else {
		hPrime1 = atan2(b1, a1Prime);
		/*
		 * This must be converted to a hue angle in degrees between 0
		 * and 360 by addition of 2􏰏 to negative hue angles.
		 */
		if (hPrime1 < 0)
			hPrime1 += deg360InRad;
	}
	if (b2 == 0 && a2Prime == 0)
		hPrime2 = 0.0;
	else {
		hPrime2 = atan2(b2, a2Prime);
		/*
		 * This must be converted to a hue angle in degrees between 0
		 * and 360 by addition of 2􏰏 to negative hue angles.
		 */
		if (hPrime2 < 0)
			hPrime2 += deg360InRad;
	}

	/*
	 * Step 2
	 */
	/* Equation 8 */
	deltaLPrime = l2 - l1;
	/* Equation 9 */
	deltaCPrime = CPrime2 - CPrime1;
	/* Equation 10 */
	CPrimeProduct = CPrime1 * CPrime2;
	if (CPrimeProduct == 0)
		deltahPrime = 0;
	else {
		/* Avoid the fabs() call */
		deltahPrime = hPrime2 - hPrime1;
		if (deltahPrime < -deg180InRad)
			deltahPrime += deg360InRad;
		else if (deltahPrime > deg180InRad)
			deltahPrime -= deg360InRad;
	}
	/* Equation 11 */
	deltaHPrime = 2.0 * sqrt(CPrimeProduct) *
	    sin(deltahPrime / 2.0);

	/*
	 * Step 3
	 */
	/* Equation 12 */
	barLPrime = (l1 + l2) / 2.0;
	/* Equation 13 */
	barCPrime = (CPrime1 + CPrime2) / 2.0;
	/* Equation 14 */
	barhPrime = hPrime1 + hPrime2;
	hPrimeSum = hPrime1 + hPrime2;
	if (CPrime1 * CPrime2 == 0) {
		barhPrime = hPrimeSum;
	} else {
		if (fabs(hPrime1 - hPrime2) <= deg180InRad)
			barhPrime = hPrimeSum / 2.0;
		else {
			if (hPrimeSum < deg360InRad)
				barhPrime = (hPrimeSum + deg360InRad) / 2.0;
			else
				barhPrime = (hPrimeSum - deg360InRad) / 2.0;
		}
	}
	/* Equation 15 */
	T = 1.0 - (0.17 * cos(barhPrime - deg2Rad(30.0))) +
	    (0.24 * cos(2.0 * barhPrime)) +
	    (0.32 * cos((3.0 * barhPrime) + deg2Rad(6.0))) -
	    (0.20 * cos((4.0 * barhPrime) - deg2Rad(63.0)));
	/* Equation 16 */
	deltaTheta = deg2Rad(30.0) *
	    exp(-pow((barhPrime - deg2Rad(275.0)) / deg2Rad(25.0), 2.0));
	/* Equation 17 */
	R_C = 2.0 * sqrt(pow(barCPrime, 7.0) /
	    (pow(barCPrime, 7.0) + pow25To7));
	/* Equation 18 */
	S_L = 1 + ((0.015 * pow(barLPrime - 50.0, 2.0)) /
	    sqrt(20 + pow(barLPrime - 50.0, 2.0)));
	/* Equation 19 */
	S_C = 1 + (0.045 * barCPrime);
	/* Equation 20 */
	S_H = 1 + (0.015 * barCPrime * T);
	/* Equation 21 */
	R_T = (-sin(2.0 * deltaTheta)) * R_C;

	/* Equation 22 */

	deltaE = sqrt(
	    pow(deltaLPrime / (k_L * S_L), 2.0) +
	    pow(deltaCPrime / (k_C * S_C), 2.0) +
	    pow(deltaHPrime / (k_H * S_H), 2.0) +
	    (R_T * (deltaCPrime / (k_C * S_C)) * (deltaHPrime / (k_H * S_H))));

	if (deltaE<tempmaxe)
	{
    tempmaxe = deltaE;
    tempmaxpos = ini;
    }
	}
	if (tempmaxpos == 1 || tempmaxpos == 2 || tempmaxpos == 3 || tempmaxpos == 4)
	{
	tempmaxpos = 0;
	}
	for (indfind=1; indfind<=8; indfind++)
	{
	indfindind = indfind*4;
	if (tempmaxpos == indfindind+1 || tempmaxpos == indfindind+2 || tempmaxpos == indfindind+3 || tempmaxpos == indfindind+4)
	{
	tempmaxpos = indfindind+1;
	}
	}
	retpos[oi] = tempmaxpos;
	}
    #pragma omp barrier
	return (retpos);
}

#ifdef __cplusplus
}
#endif
//int main()
//{
//cout<<CIEDE2000(1.,1.,1.,1.,1.,2.);
//return 1;
//}