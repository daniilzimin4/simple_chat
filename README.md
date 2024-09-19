# simple_chat
##### How to run it:
1. Run server ```python server.py```
2. Open chat in browser: http://127.0.0.1:5000/
3. Check number of messages http://127.0.0.1:5000/messages/count

##### How to test it:
```python -m unittest test_app.py```

##### Stress test:
```
    C 8:0 FlaskAppTests - A (2)
    M 21:4 FlaskAppTests.stress_test - A (2)
    M 9:4 FlaskAppTests.setUp - A (1)
    M 16:4 FlaskAppTests.tearDown - A (1)
    M 32:4 FlaskAppTests.test_time_behavior - A (1)
    M 40:4 FlaskAppTests.test_recoverability - A (1)
    M 60:4 FlaskAppTests.test_maintainability - A (1)
    M 70:4 FlaskAppTests.test_disconnection_recovery - A (1)
    M 99:4 FlaskAppTests.test_code_complexity - A (1)

9 blocks (classes, functions, methods) analyzed.
Average complexity: A (1.2222222222222223)

Code Complexity Analysis for server.py:
server.py
    F 25:0 get_messages - A (2)
    F 21:0 home - A (1)
    F 30:0 count_messages - A (1)
    F 35:0 handle_send_message - A (1)
    C 12:0 Message - A (1)

5 blocks (classes, functions, methods) analyzed.
Average complexity: A (1.2)

.Average execution time for test_disconnection_recovery: 0.0372 seconds
.Average execution time for test_maintainability: 0.0001 seconds
.Average execution time for test_recoverability: 0.0312 seconds
.Average execution time for test_time_behavior: 0.0003 seconds
.
----------------------------------------------------------------------
Ran 5 tests in 0.892s

OK

```
