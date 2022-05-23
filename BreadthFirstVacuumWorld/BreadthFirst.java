import java.util.*;
public class BreadthFirst{
	
	int inputState;
	int [] children, stateChildren;
	int child;
	ArrayList<Integer> frontier = new ArrayList<Integer>();
	ArrayList<Integer> explored = new ArrayList<Integer>();
	
	
	//setting the children of each of the vacuum world states
	private int[] getStateChildren(int inputState) {
		if(inputState == 1) {
			int[] children = {1, 2, 3};
			return children;
			
		}else if(inputState == 2) {
			int[] children = {1, 2, 6};
			return children;
			
		}else if(inputState == 3) {
			int[] children = {3, 4, 3};
			return children;
			
		}else if(inputState == 4) {
			int[] children = {3, 4, 8};
			return children;
			
		}else if(inputState == 5) {
			int[] children = {5, 6, 7};
			return children;
			
		}else if(inputState == 6) {
			int[] children = {5, 6, 6};
			return children;
			
		}else if(inputState == 7) {
			int[] children = {7, 8, 7};
			return children;
			
		}else if(inputState == 8) {

			int[] children = {7, 8, 8};
			return children;
		}else {
			return null;
		}
	}
	
	//checking if a state is a goal state
	private static boolean checkGoalState(int inputState){
		if(inputState == 7 || inputState == 8) {
			return true;
		}else {
			return false;
		}
	}	
	
	//adding state to end of  frontier, if it doesnt already appear in explored states
	private void enqueueFrontier(int inputState) {
		if(!explored.contains(inputState) && !frontier.contains(inputState)) {
			frontier.add(inputState);
			
		}else {
			;
		}
	}
	
	
	//get frontier head
	private int getFrontierHead() {
		return frontier.get(0);
	}
	
	private void dequeueFrontier() {
		frontier.remove(0);
	}
	
	//adding initial input state to explored states
	private void addExplored(int inputState) {
		explored.add(inputState);

	}
	
	//using overloading for enqueue for an array of states
	private void enqueueFrontier(int[] children) {
		for(int child: children) {
			if(!explored.contains(child) && !frontier.contains(child)) {
				frontier.add(child);
				System.out.println("Adding " + child + " to frontier");
			}else {
				System.out.println("Not adding " + child + " to frontier");
			}
		}
	}
	
	void runAlgo(int inputState) {
		//initially adding input state to frontier
		enqueueFrontier(inputState);
		System.out.println("Initial state " + inputState);
		//getting the children of that state
		int [] firstChildren = getStateChildren(inputState);
		System.out.println("State " + inputState + " has children " + Arrays.toString(firstChildren));
		enqueueFrontier(getStateChildren(inputState));
		
		System.out.println("Initial frontier " + frontier);
		System.out.println("Initial explored" + explored);
		//loop to make algorithm keep looping until the frontier is empty
		while(frontier.size() != 0) {
			int currentState = getFrontierHead();
			
			System.out.println("Current state being computed is State " + currentState);
			System.out.println("Current frontier " + frontier);
			System.out.println("Current explored" + explored);
			
			int[] currentChildren = getStateChildren(currentState);
			System.out.println("Checking if children " + Arrays.toString(currentChildren) + " should be added to frontier");
			//add children to the frontier
			enqueueFrontier(getStateChildren(currentState));
			//remove from the frontier queue
			dequeueFrontier();
			//if goal state reached, algorithm breaks, otherwise it goes to next state in the frontier
			if(checkGoalState(currentState)) {
				System.out.println("Goal state State " + currentState + " reached, both rooms are clean!");
				break;
				
			}else {
				addExplored(currentState);
				System.out.println("State " + currentState + " is not a goal state\nChecking next state...");
			}
		}
		
		
		
		
	}
	
	
	
	public static void main(String[] args) {
		 
		Scanner sc = new Scanner(System.in);
		//initialising the object
		BreadthFirst bf = new BreadthFirst();
		//simple scanner to input initial state for completeness
		System.out.print("Enter an initial vacuum state to compute the search (Integer 1-8): ");
		int userInput = sc.nextInt();
		System.out.println("--------------------------------------------");
		bf.runAlgo(userInput);
		
		
	}
	
	
	
}
