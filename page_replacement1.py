# Added FIFO algorithm
# Simple Page Replacement Simulator: FIFO, LRU, Optimal
# Usage: python3 page_replacement.py
# feature test edit


def fifo(pages, frames, verbose=False):
    memory = []
    faults = 0
    frame_states = []

    for p in pages:
        if p not in memory:
            faults += 1
            if len(memory) < frames:
                memory.append(p)
            else:
                memory.pop(0)
                memory.append(p)
        # record state for optional display
        if verbose:
            frame_states.append(list(memory))
    return faults, frame_states

# LRU algorithm
def lru(pages, frames, verbose=False):
    memory = []
    faults = 0
    frame_states = []
    # We'll keep memory list such that oldest (LRU) is at index 0, newest at end.
    for p in pages:
        if p in memory:
            # make it most recently used: remove and append
            memory.remove(p)
            memory.append(p)
        else:
            faults += 1
            if len(memory) < frames:
                memory.append(p)
            else:
                # remove least recently used (index 0)
                memory.pop(0)
                memory.append(p)
        if verbose:
            frame_states.append(list(memory))
    return faults, frame_states

def optimal(pages, frames, verbose=False):
    memory = []
    faults = 0
    frame_states = []

    for i, p in enumerate(pages):
        if p not in memory:
            faults += 1
            if len(memory) < frames:
                memory.append(p)
            else:
                # choose page in memory that is used farthest in future (or not used again)
                future = pages[i+1:]
                replace = None
                far_index = -1
                for m in memory:
                    if m not in future:
                        replace = m
                        break
                    else:
                        idx = future.index(m)
                        if idx > far_index:
                            far_index = idx
                            replace = m
                memory.remove(replace)
                memory.append(p)
        if verbose:
            frame_states.append(list(memory))
    return faults, frame_states

def hit_ratio(total_refs, faults):
    hits = total_refs - faults
    return hits / total_refs if total_refs > 0 else 0

def main():
    try:
        pages = list(map(int, input("Enter pages (space separated): ").strip().split()))
        frames = int(input("Enter number of frames: ").strip())
    except Exception as e:
        print("Invalid input. Example page input: 7 0 1 2 0 3 0 4 2 3 0 3")
        return

    n = len(pages)
    f_fifo, s_fifo = fifo(pages, frames)
    f_lru, s_lru = lru(pages, frames)
    f_opt, s_opt = optimal(pages, frames)

    print("\n--- Results ---")
    print(f"Total references: {n}")
    print(f"FIFO  -> Page Faults: {f_fifo}, Hit Ratio: {hit_ratio(n,f_fifo):.2f}")
    print(f"LRU   -> Page Faults: {f_lru}, Hit Ratio: {hit_ratio(n,f_lru):.2f}")
    print(f"Optimal -> Page Faults: {f_opt}, Hit Ratio: {hit_ratio(n,f_opt):.2f}")
    print("FIFO simulation completed")


    results = {"FIFO": f_fifo, "LRU": f_lru, "Optimal": f_opt}
    best = min(results, key=results.get)

    # Comparing algorithms

    print(f"\nBest algorithm for given input: {best} with {results[best]} page faults")
    
    # Optional: show frame states for one algorithm (uncomment to show)
    # print("\nFrame states for FIFO (after each reference):")
    # for state in s_fifo:
    #     print(state)



if __name__ == "__main__":
    main()
# End of project


