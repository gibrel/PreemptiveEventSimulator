import tests.test1_match_sim as t1
import tests.test2_insert_city_data as t2
import tests.test3_insert_sports as t3
import tests.test4_import_and_create as t4
import tests.test5_search as t5
import tests.test6_redundant_insertion as t6
import tests.test7_list_with_lambda_filter as t7
import tests.test8_distribution as t8
import tests.test9_curses as t9
import tests.test10_curses_colors as t10
import tests.test11_curses_debug as t11
import tests.test12_curses_tutorial as t12

tests = [t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12]

if __name__ == '__main__':
    # Run tests
    print("#################################\n"
          "#####     Running tests     #####\n"
          "#################################\n")
    for test in tests:
        test.test()