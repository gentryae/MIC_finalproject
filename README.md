# Petrinet Model Background
This is an example Design studio aimed for developers relatively new to the [WebGME](https://webgme.org) platform.

It allows model editing, simulation, and some limited model-checking functionality.

The studio implements a petrinet domain. A petrinet is a graph of two things – places and transitions. Places may contain tokens.  Transitions are considered enabled when all of its inplaces (the places that are inputs to the transition) have a token. In this model, places are white circles, transitions are black skinny rectangles, and tokens are black small circles. 

 In a broad sense, petrinets can be used to model many things by treating tokens as an instance, places as a state in which those tokens may be, and transitions as an action that may alter the state of that token. This is visualized by a token leaving one place, through a transition, and entering a new place. Creating a model in the domain can help increase understanding of model boundaries, model processes/order, and determine if there are areas of possible deadlock. 

For example, the test example model models mixing two colors – red and blue – to create purple. It has a red place, a blue place, a ‘mix’ transition and a purple place. When a token is populated into only the red or blue place, it cannot proceed through the ‘mix’ transition. Once at least one token is in both the red and blue place, the mix transition is enabled and the user can enact it so that the tokens move through the connections to the purple place. This model could help users understand the ratio of resources (red vs blue) to create the result end product. This example has a very simple ratio and process, but petrinets can be scaled up to more complex models. Furthermore, the benefits of using this model tool will increase exponentially as the model complexity increases. 

Petrinet models may be classified into four common classifications – free choice, marked graph, state machine and workflow. A petrinet model is free choice if every transition has a unique set of inplaces. A petrinet model is a marked graph if every place has exactly one input and one output. On the other hand, a petrinet is a state machine if every transition has exactly one input and one output.  Lastly, a petrinet is a work flow if there is one start and end point (start has only outputs, end has only inputs) and every place is reachable along a path from the start to end point. A petrinet model may be classified into just one, multiple, or none of these classifications. 


# Model Installation
You will need the following to use this studio: 
-	Npm
-	Docker
-	mongoDB
-	IDE

To install this design studio, you need to first download or clone the github repo locally your machine. In the terminal of the project, you need to run “npm install”. To use the plug-in, you’ll also need to run “pip install webgme_bindings”. Then, start docker and create an instance to run on Port 27017. You can open the code in your IDE (VScode is recommended and has a useful mongoDB extension) – ensure that the default python path is correct. 

Once you are ready to run, in the terminal type 'npm run start. Then, you can open your internet browser and type ‘localhost:8888/’ and press enter. WebGME will open up and you can open up the already created project final_proj_gentry, or create a new project with final_proj_gentry as the starting seed. 

You can also just navigate to webgme in your browser, create an account, create a new project from import and choose the final_proj_gentry_import.webgmex file. Then you can use that model on the web instead of using one locally.

# Model Use
When the model opens, you can familiarize yourself with the basic building blocks and rules of a petrinet by looking at the meta tab. Click the Meta option on the left-hand side of the page and then click on the Petrinet tab at the top of the page. This tab is where you can build the ‘global rules’ of the backbone for a model.

After familiarizing with the meta model, you can look at some of the example models such as test, MarkedGraph, StateMachine, FreeChoice and Workflow. You can go ‘into’ these blocks via double clicking or clicking on the block and then clicking the arrow icon in the left upper corner. You can alter these diagrams by dragging Place or Transition components that are on the left-hand side. You can add tokens to a Place by going into the place component, and then dragging tokens from the left-hand side. You can create entirely new petrinet examples by going back to ROOT and dragging a Petrinet component onto the screen, going into that component, and adding the required Places, Transitions and Tokens. To go back to the root or graph view from within a component, you can click on the label of your current element that is in the navigation bar at the top of the page. 

You can create simulations, determine what (if any) petrinet classification the model is, and determine if there are points of deadlock of an Composition model by using the SimSM option on the left hand side. At the top toolbar, a play button will appear if only one transition is enabled. Hitting the play button will fire the transition. If multiple transitions are possible, a drop down option will appear that allows the user to choose which transition to enable. The reverse button will revert the simulation back to the starting state – which is determined by the Composition model. The question mark icon will run the plugin which determines the petrinet classification. When run, a notification of the classification will pop up in the bottom right corner of the screen on the Notifications bar. 

