/******************************************************************
*                                                                 *
* Copyright (C) 2015-2017 by DarkGengar                           *
* This file is part of {Project}                              	  *
*                                                                 *
* {Project} is free software.                                     *
* You can redistribute or modify it under the terms               *
* of the GNU Lesser General Public License as published           *
* by the Free Software Foundation, either                         *
* version 3 of the License, or (at your option) any               *
* later version provided you include a copy of the                *
* licence and this header.                                        *
* See GNU GENERAL PUBLIC LICENSE for more details.                *
*                                                                 *
* {Project} is redistributed to help you with                     *
* your next projects, but WITHOUT ANY WARRANTY;                   *
* without even the implied warranty of                            *
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.            *
*                                                                 *
* You should have received a copy of                              *
* the GNU GENERAL PUBLIC LICENSE along with {Project}.            *
* If you not have a copy of the                                   *
* GNU GENERAL PUBLIC LICENSE see: http://www.gnu.org/licenses     *
*                                                                 *
******************************************************************/
 
/**
*  \file       types.h
*  \date	   30 April 2017
*  \author	   DarkGengar
*  \brief	   AGB Types Include
*
*  \details  This is a AGB type include file.
*/

#ifndef TYPES_H
#define TYPES_H

#ifdef __cplusplus
extern "C"
{
#endif

#define NULL 0
#define TRUE 1
#define FALSE 0

#define SCREEN_WIDTH 	240
#define SCREEN_HEIGHT 	160

// Unsigned
typedef unsigned char  u8,  byte;
typedef unsigned short u16, hword;
typedef unsigned int   u32, word;
typedef unsigned long long u64;

// Signed
typedef signed char  s8;
typedef signed short s16; 
typedef signed int   s32;
typedef signed long long s64;

typedef float f32;
typedef double f64;

// Volatiles Unsigned
typedef volatile u8  vu8;
typedef volatile u16 vu16;
typedef volatile u32 vu32;
typedef volatile u64 vu64;

// Volatiles Signed
typedef volatile s8  vs8;
typedef volatile s16 vs16;
typedef volatile s32 vs32;
typedef volatile s64 vs64;

typedef u16 COLOR;

#define INLINE static inline

#ifdef __cplusplus	
}
#endif


#endif // TYPES_H
