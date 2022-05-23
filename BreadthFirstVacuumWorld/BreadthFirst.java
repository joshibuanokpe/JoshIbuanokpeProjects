import java.util.*;
public class BreadthFirst{
	
	int inputState, leftChild, rightChild, suckChild;
	//private ArrayList<Integer> frontier;
	//private ArrayList<Integer> explored;
	int [] children, stateChildren;
	int child;
	ArrayList<Integer> frontier = new ArrayList<Integer>();
	ArrayList<Integer> explored = new ArrayList<Integer>();
	
	
	//setting the children of each of the vacuum world states
	private int[] getStateChildren(int inputState) {
		if(inputState == 1) {
			leftChild = 1;
			rightChild = 2;
			suckChild = 3;
			int[] children = {1, 2, 3};
			return children;
			
		}else if(inputState == 2) {
			leftChild = 1;
			rightChild = 2;
			suckChild = 6;
			int[] children = {1, 2, 6};
			return children;
			
		}else if(inputState == 3) {
			leftChild = 3;
			rightChild = 4;
			suckChild = 3;
			int[] children = {3, 4, 3};
			return children;
			
		}else if(inputState == 4) {
			leftChild = 3;
			rightChild = 4;
			suckChild = 8;
			int[] children = {3, 4, 8};
			return children;
			
		}else if(inputState == 5) {
			leftChild = 5;
			rightChild = 6;
			suckChild = 7;
			int[] children = {5, 6, 7};
			return children;
			
		}else if(inputState == 6) {
			leftChild = 5;
			rightChild = 6;
			suckChild = 6;
			int[] children = {5, 6, 6};
			return children;
			
		}else if(inputState == 7) {
			leftChild = 7;
			rightChild = 8;
			suckChild = 7;
			int[] children = {7, 8, 7};
			return children;
			
		}else { //if(inputState == 8) {
			leftChild = 7;
			rightChild = 8;
			suckChild = 8;
			int[] children = {7, 8, 8};
			return children;
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
		enqueueFrontier(inputState);
		//addExplored(inputState);
		//System.out.println("Initial frontier " + frontier);
		System.out.println("Initial state " + inputState);
		int [] firstChildren = getStateChildren(inputState);
		System.out.println(inputState + " has children " + Arrays.toString(firstChildren));
		enqueueFrontier(getStateChildren(inputState));
		
		System.out.println("Initial frontier " + frontier);
		System.out.println("Initial explored" + explored);
		
		while(frontier.size() != 0) {
			int currentState = getFrontierHead();
			
			System.out.println("Current state being computed is State " + currentState);
			System.out.println("Current frontier " + frontier);
			System.out.println("Current explored" + explored);
			
			int[] currentChildren = getStateChildren(currentState);
			System.out.println("Adding " + Arrays.toString(currentChildren) + " to frontier");
			enqueueFrontier(getStateChildren(currentState));
			dequeueFrontier();
			if(checkGoalState(currentState)) {
				System.out.println("Goal state State " + currentState + " reached, both rooms are clean!");
				break;
				//return currentState;
			}else {
				addExplored(currentState);
				System.out.println("State " + currentState + " is not a goal state\nChecking next state...");
				//dequeueFrontier();
			}
			//dequeueFrontier();
		}
		
		
		
		
	}
	
	
	
	public static void main(String[] args) {
		 
		Scanner sc = new Scanner(System.in);
		BreadthFirst bf = new BreadthFirst();
		
		System.out.print("Enter an initial vacuum state to compute the search (Integer 1-8): ");
		int userInput = sc.nextInt();
		bf.runAlgo(userInput);
		
		
	}
	
	
	
}
