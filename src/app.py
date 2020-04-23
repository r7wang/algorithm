from src import array

# arr = array.make_2d_array_yx_seeded_col_order_alternating_using_iter([1, 3, 4, 7, 6, 2, 9, 5], 3, 3)
# arr = array.make_2d_array_yx_seeded_col_order_alternating_using_inf(5, 5)
arr = array.make_2d_array_yx_unseeded_col_order_alternating_using_inf(5, 5)
arr2 = array.copy_2d_array(arr)
array.mult_2d_array_in_place(arr, 3)
array.print_2d_yx(arr)
array.print_2d_yx(arr2)
