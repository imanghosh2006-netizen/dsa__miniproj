def calculate_stock_span(prices):
    n = len(prices)
    span = [0] * n
    stack = []  # Stores indices of days

    for i in range(n):
        # Pop elements from stack while stack is not empty and top is <= current price
        while stack and prices[stack[-1]] <= prices[i]:
            stack.pop()

        # If stack becomes empty, price[i] is greater than all elements to its left
        span[i] = (i + 1) if not stack else (i - stack[-1])

        # Push current index to stack
        stack.append(i)

    return span

def visualize_stock_span(prices, spans):
    print("\n" + "="*60)
    print(f"{'Day':<6} | {'Price ($)':<10} | {'Span':<6} | {'Price & Span Visual'}")
    print("="*60)
    for i in range(len(prices)):
        bar = "█" * (prices[i] // 5)
        span_indicator = f"(+{spans[i]}d)"
        print(f"Day {i+1:<2} | ${prices[i]:<9} | {spans[i]:<6} | {bar} {span_indicator}")
    print("="*60 + "\n")

def main():
    print("--- Real-Time Stock Span Visualizer ---")
    # Pre-loaded sample data for quick demo
    sample_prices = [100, 80, 60, 70, 60, 75, 85, 110]
    
    choice = input("Use sample stock data [100, 80, 60, 70, 60, 75, 85, 110]? (y/n): ").strip().lower()
    if choice == 'y':
        prices = sample_prices
    else:
        raw = input("Enter stock prices separated by spaces (e.g., 100 80 60 70): ")
        prices = [int(x) for x in raw.strip().split()]

    spans = calculate_stock_span(prices)
    visualize_stock_span(prices, spans)

    # Real-time live addition loop for video demo
    while True:
        new_price = input("Enter next day's live stock price (or 'q' to quit): ").strip()
        if new_price.lower() == 'q':
            break
        if new_price.isdigit():
            prices.append(int(new_price))
            spans = calculate_stock_span(prices)
            visualize_stock_span(prices, spans)
        else:
            print("Invalid input. Enter a positive integer.")

if __name__ == "__main__":
    main()