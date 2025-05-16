def main():
    file_path= "overhead.txt"
    avg_diff = 0
    diffs = []
    count = 0
    sum = 0
    # compare
    with open(file_path, "r") as file:
        lines = file.readlines()
        count = len(lines)
        for line in lines:
            line = line.strip()
            
            times = line.split("|")
            
            diff = float(times[1]) - float(times[0])
            sum += diff
            diffs.append(diff)
            
    ### get avg diff
    avg = sum / count
    print(f"average websocket message overhead: {avg}")
        
if __name__ == "__main__":
    main()