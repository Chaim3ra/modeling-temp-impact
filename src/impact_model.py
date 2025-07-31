from typing import List, Tuple


def compute_slippage(
        asks: List[Tuple[float, int]],
        mid_price: float,
        order_size: int
        ) -> float:
    """
    Walking the book and calculating slippage to simulate temporary impact g_t(x)
    """

    uniflled_orders = order_size
    diff = 0.0

    for price, size in asks:
        # no. of shares that can be filled from the current level
        curr_fill = min(uniflled_orders, size)
        # (p_k - m_t) * delta x_k 
        diff += (price - mid_price) * curr_fill
        uniflled_orders -= curr_fill

        # if all orders have been filled
        if uniflled_orders == 0:
            break


    # if there are still some unfilled orders after walking the entire ask-side queue
    if uniflled_orders > 0:
        raise ValueError(f"Insufficient ask-side depth to fill {order_size} shares")
        

    # slippage per share
    slippage = diff / order_size
    return slippage

