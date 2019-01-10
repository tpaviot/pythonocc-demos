# start xvfb
export DISPLAY=:99.0
sh -e /etc/init.d/xvfb start
sleep 3 # give xvfb some time to start
# run example as tests
python run_examples_as_tests.py
