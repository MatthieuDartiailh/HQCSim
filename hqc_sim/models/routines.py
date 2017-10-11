# -*- coding: utf-8 -*-
"""Numba optimized array manipulation routines.

"""
from numba import njit


@njit
def fill_array2d_from_column(arr, i, data):
    """Fill the last axis of the array using the provided column.

    Parameters
    ----------
    arr : ndarray
        Two dimensional array to fill.

    i : int
        Index of the line to fill.

    data : ndarray
        One dimensional array whose values should be copied in arr.

    """
    for j in range(len(data)):
        arr[i, j] = data[j]


@njit
def fill_array3d_from_matrix(arr, i, data):
    """Fill array two last axis using a bidimensional array.

    Parameters
    ----------
    arr : ndarray
        Array to fill.

    i : int
        Index of the first axis which should be filled.

    data : ndarray
        Bidimensional array to copy into arr.

    """
    for j in range(data.shape[0]):
        for k in range(data.shape[1]):
            arr[i, j, k] = data[j, k]


@njit
def fill_array3d_from_column(arr, i, j, data):
    """Fill the last axis of the array using the provided column.

    Parameters
    ----------
    arr : ndarray
        Three dimensional array to fill.

    i : int
        Index of the line to fill.

    j : int
        Index of the column to fill.

    data : ndarray
        One dimensional array whose values should be copied in arr.

    """
    for k in range(len(data)):
        arr[i, j, k] = data[k]


@njit
def fill_array4d_from_matrix(arr, i, j, data):
    """Fill array two last axis using a bidimensional array.

    Parameters
    ----------
    arr : ndarray
        4 dimension array to fill.

    i : int
        Index of the first axis which should be filled.

    i : int
        Index of the second axis which should be filled.

    data : ndarray
        Bidimensional array to copy into arr.

    """
    for k in range(data.shape[0]):
        for l in range(data.shape[1]):
            arr[i, j, k, l] = data[k, l]


@njit
def fill_column_from_array2d(col, arr, i):
    """Fill 1d array from a 2d array line.

    Parameters
    ----------
    col : ndarray
        1D array to fill.

    arr : ndarray
        Array from which to gather the data.

    i : int
        Index of the line to copy into col.

    """
    for j in range(len(col)):
        col[j] = arr[i, j]


@njit
def fill_column_from_array3d(col, arr, i, j):
    """Fill 1d array from a 3d array last axis.

    Parameters
    ----------
    col : ndarray
        1D array to fill.

    arr : ndarray
        Array from which to gather the data.

    i : int
        Index of the line to copy into col.

    j : int
        Index of the line to copy into col.

    """
    for k in range(len(col)):
        col[k] = arr[i, j, k]


@njit
def fill_matrix_from_array3d(mat, arr, i):
    """Fill 2d array from a 3d array last axis.

    Parameters
    ----------
    mat : ndarray
        2D array to fill.

    arr : ndarray
        Array from which to gather the data.

    i : int
        Index of the line to copy into mat.

    """
    for j in range(mat.shape[0]):
        for k in range(mat.shape[1]):
            mat[j, k] = arr[i, j, k]


@njit
def fill_matrix_from_array4d(mat, arr, i, j):
    """Fill 2d array from a 4d array last axis.

    Parameters
    ----------
    mat : ndarray
        2D array to fill.

    arr : ndarray
        Array from which to gather the data.

    i : int
        Index of the line to copy into mat.

    j : int
        Index of the line to copy into mat.

    """
    for k in range(mat.shape[0]):
        for l in range(mat.shape[1]):
            mat[k, l] = arr[i, j, k, l]


@njit
def index_sort(arr, index):
    """Compute the index sorting a 1d array.

    Parameters
    ----------
    arr : ndarray
        Array on which to base the sorting.

    index : ndarray
        Array in which to write the index sorting the array.

    """
    n_sorted = 0
    i_sorted = 0
    aux = len(index)
    mini = 0.
    for i in range(aux):
        if arr[i] < arr[i_sorted]:
            i_sorted = i
    index[n_sorted] = i_sorted
    mini = arr[i_sorted]
    n_sorted += 1
    i_sorted = n_sorted

    while n_sorted < aux:
        for i in range(aux):
            if arr[i_sorted] <= mini or mini < arr[i] < arr[i_sorted]:
                i_sorted = i
        index[n_sorted] = i_sorted
        mini = arr[i_sorted]
        n_sorted += 1
        i_sorted = n_sorted
