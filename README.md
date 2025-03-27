# ai_temp_monitor

In this project an 

## The structure

The main function run asynchronously two parts of the program. A graph to visualize the streaming of the data and the program that check the stream and call the ai agent in case anomalies are detected.
More into detail, each new data provided by the streaming is checked if it lies inside the upper and lower threshold. Each time a warning is generated, on another thread, the agent is called. The agent will charge all the warning that have been registered and, using tools to retrieve more information, it will try to create an hypothesis on the possible causes of the temperature variation.
For the moment the only tool created will check the average temperature of the week. But it is easy to add tools to the agent. For example it could be interesting to add a tool that 

## AI agent

The agent consists of an LLM (gemini-2.0-flash) that has the role of orchestrator of tools it can be provided with. A tool can be a simply API call, or another ai agent.
The orchestrator chooses the tools to use to analise the warnings it gets and try to 

## The dataset

The data are mock data obtain from (kaggle link).
Of all the data we keep just the temperature for simplicity. And the timestamp of the date is generated when the data are read from the csv file.


