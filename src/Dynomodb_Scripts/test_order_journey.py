import sys
from order_journey import (
    create_order_from_user,
    create_packer,
    assign_order_to_packer,
    packer_check_and_process_order,
    assign_order_to_rider,
    get_order
)
from colorama import Fore, Style, init
init(autoreset=True)

def print_test_banner(text):
    width = 70
    print("\n" + "#" * width)
    print(text.center(width, " "))
    print("#" * width + "\n")

def test_order_journey():
    total_tests = 5
    passed = 0
    failed = 0
    print_test_banner("TEST: ORDER JOURNEY START")
    # Step 1: User places order
    try:
        order_id = create_order_from_user()
        order = get_order(order_id)
        assert order is not None, "Order should exist after creation."
        assert order['status'] == 'unpacked', "Order status should be 'unpacked' after creation."
        print(Fore.GREEN + "PASS: Order created and status is 'unpacked'.")
        passed += 1
    except AssertionError as e:
        print(Fore.RED + f"FAIL: {e}")
        failed += 1
        order_id = None
    # Step 2: Create packer
    try:
        packer_id = create_packer()
        print(Fore.GREEN + "PASS: Packer created.")
        passed += 1
    except Exception as e:
        print(Fore.RED + f"FAIL: {e}")
        failed += 1
        packer_id = None
    # Step 3: Assign order to packer
    try:
        assign_order_to_packer(order_id, packer_id)
        order = get_order(order_id)
        assert order['packerId'] == packer_id, "Order should be assigned to the correct packer."
        print(Fore.GREEN + "PASS: Order assigned to packer.")
        passed += 1
    except AssertionError as e:
        print(Fore.RED + f"FAIL: {e}")
        failed += 1
    # Step 4: Packer checks and processes order
    try:
        before_status = order['status']
        order = packer_check_and_process_order(order_id)
        after_status = order['status']
        print(f"Order status before packing: {before_status}")
        print(f"Order status after packing: {after_status}")
        assert after_status == 'packed', "Order status should be 'packed' after processing."
        print(Fore.GREEN + "PASS: Order packed by packer.")
        passed += 1
    except AssertionError as e:
        print(Fore.RED + f"FAIL: {e}")
        failed += 1
    # Step 5: Assign order to rider
    try:
        order = assign_order_to_rider(order_id)
        assert 'riderId' in order, "Order should have a riderId after assignment."
        assert order['status'] == 'assigned_to_rider', "Order status should be 'assigned_to_rider' after rider assignment."
        print(Fore.GREEN + "PASS: Order assigned to rider.")
        passed += 1
    except AssertionError as e:
        print(Fore.RED + f"FAIL: {e}")
        failed += 1
    print_test_banner("TEST: ORDER JOURNEY END")
    print("\n==================== TEST SUMMARY ====================")
    print(f"Total tests:   {total_tests}")
    print(Fore.GREEN + f"Passed:        {passed}")
    print(Fore.RED + f"Failed:        {failed}")
    print("====================================================\n")
    if failed > 0:
        sys.exit(1)

if __name__ == "__main__":
    try:
        test_order_journey()
    except Exception as e:
        print(f"\nERROR: {e}")
        sys.exit(2) 