python deepQ.py --env CarRacing-v0 --proto cfn\CarRacing-v0.prototxt --game_skip 50 --n_steps 4000000 --momentum 0.950000 --learning_rate 0.001000 --discount 0.950000 --epsilon_min 0.100000 --epsilon_max 1.000000 --epsilon_steps 1000000 --n_prev_states 100000 --checkpoint_interval 1000 --target_update_interval 5000 --learning_interval 1 --minibatch_size 50 --max_neg_reward_steps 150 --save_rewards 