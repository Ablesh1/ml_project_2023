import numpy as np
import websockets
import json
import asyncio
import logic_2048


async def game_engine(websocket):
    """
    This function is the "heart" of the game. It waits for a 2D array and then
    performs transformation and then sends a result with status code to the client.

    Args:
        websocket:  object used to set up websocket server. The expected return should be a json
                    containing game board, swiping direction and seed, which is a boolean determining
                    if we start a new game

    Sends:
        board: transformed 2D matrix containing powers of 2
        statusCode: 0 if we can play further, 1 if we win, 255 if we lose
        topValue: biggest value in the matrix - used for color manipulation

    Returns:
        void
    """
    status_code = 0

    # Wait for input and then transform json to dict
    web_json = await websocket.recv()
    print(f"<<< {web_json}")
    web_dict = json.loads(web_json)

    game_matrix = web_dict["board"]
    web_input = web_dict["direction"]
    is_init = web_dict["seed"]
    score = web_dict["points"]

    game_matrix = np.array(game_matrix)

    if is_init:
        game_matrix = logic_2048.place_new(game_matrix)
        print(game_matrix)

    # Single game step
    game_matrix, success, top_value, total_score, _ = logic_2048.transform_matrix(
        game_matrix, web_input, score, True
    )
    print(game_matrix)

    if logic_2048.win_check(game_matrix):
        # If client wins, construct result json with status code 1 and send via websocket
        print("CONGRATS! YOU WON!")
        status_code = 1
        result = {
            "board": game_matrix,
            "statusCode": status_code,
            "topValue": top_value,
            "score": total_score,
        }
        result = json.dumps(result)

        await websocket.send(result)
        print(f">>> {result}")
    elif not success:
        # If client loses, construct result json with status code 255 and send via websocket
        print("Game over")
        status_code = 255
        result = {
            "board": game_matrix,
            "statusCode": status_code,
            "topValue": top_value,
            "score": total_score,
        }
        result = json.dumps(result)

        await websocket.send(result)
        print(f">>> {result}")
        return 0
    else:
        # If client can continue to play, construct result json with status code 0 and send via websocket
        result = {
            "board": game_matrix,
            "statusCode": status_code,
            "topValue": top_value,
            "score": int(total_score),
        }
        result = json.dumps(result)

        await websocket.send(result)
        print(f">>> {result}")


async def main():
    async with websockets.serve(game_engine, "localhost", 8765):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
