# -*- coding: utf-8 -*-
import numpy as np
from hqc_sim.models.routines import (fill_array2d_from_column,
                                     fill_array3d_from_matrix,
                                     fill_array3d_from_column,
                                     fill_array4d_from_matrix,
                                     fill_column_from_array2d,
                                     fill_matrix_from_array3d,
                                     fill_column_from_array3d,
                                     fill_matrix_from_array4d,
                                     index_sort)


def test_fill_a2d_col():
    a = np.zeros((2, 2))
    b = np.array([1, 2])
    fill_array2d_from_column(a, 1, b)
    np.testing.assert_array_equal(a, np.array([[0, 0], [1, 2]]))


def test_fill_a3d_mat():
    a = np.zeros((2, 2, 2))
    b = np.array([[1, 2], [3, 4]])
    fill_array3d_from_matrix(a, 1, b)
    np.testing.assert_array_equal(a, np.array([[[0, 0], [0, 0]],
                                               [[1, 2], [3, 4]]]))


def test_fill_a3d_col():
    a = np.zeros((2, 2, 2))
    b = np.array([1, 2])
    fill_array3d_from_column(a, 1, 0, b)
    np.testing.assert_array_equal(a, np.array([[[0, 0], [0, 0]],
                                               [[1, 2], [0, 0]]]))


def test_fill_a4d_mat():
    a = np.zeros((2, 2, 2, 2))
    b = np.array([[1, 2], [3, 4]])
    fill_array4d_from_matrix(a, 1, 0, b)
    np.testing.assert_array_equal(a, np.array([[[[0, 0], [0, 0]],
                                                [[0, 0], [0, 0]]],
                                               [[[1, 2], [3, 4]],
                                                [[0, 0], [0, 0]]]]))


def test_fill_col_a2d():
    a = np.zeros(2)
    b = np.array([[1, 2], [3, 4]])
    fill_column_from_array2d(a, b, 0)
    np.testing.assert_array_equal(a, np.array([1, 2]))


def test_fill_col_a3d():
    a = np.zeros(2)
    b = np.array([[[1, 2], [3, 4]], [[0, 0], [0, 0]]])
    fill_column_from_array3d(a, b, 0, 1)
    np.testing.assert_array_equal(a, np.array([3, 4]))


def test_fill_mat_a3d():
    a = np.zeros((2, 2))
    b = np.array([[[1, 2], [3, 4]], [[0, 0], [0, 0]]])
    fill_matrix_from_array3d(a, b, 0)
    np.testing.assert_array_equal(a, np.array([[1, 2], [3, 4]]))


def test_fill_mat_a4d():
    a = np.zeros((2, 2))
    b = np.array([[[[0, 0], [0, 0]],
                   [[0, 0], [0, 0]]],
                  [[[1, 2], [3, 4]],
                   [[0, 0], [0, 0]]]])
    fill_matrix_from_array4d(a, b, 1, 0)
    np.testing.assert_array_equal(a, np.array([[1, 2], [3, 4]]))


def test_order_index():
    ind = np.zeros(6, dtype=int)
    vec = np.array([2, 1, 3, 5, 4, 6])
    index_sort(vec, ind)
    np.testing.assert_array_equal(ind, np.array([1, 0, 2, 4, 3, 5]))
