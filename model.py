import streamlit as st 
from openai import OpenAI
import json

# client : OpenAI = OpenAI()


def update_map(latitude,longitude, zoom):
    """Move the Plotly map to given coordinates

    latitude: float
        Latitude coordinate of new center.
    longitude: float
        Longitude coordinate of new center.
    zoom: int
        Zoom level of the map after moving center.
    """

    st.session_state['map']={
        'latitude':latitude,
        'longitude':longitude,
        'zoom':zoom
    }
    return 'Map updated'
    
    
tool_to_funtion = {
    "update_map":update_map
}

def on_text_input():
    message = client.beta.threads.messages.create(
        thread_id=st.session_state["thread"].id,
        role="user",
        content=st.session_state["input_user_msg"],
    )
    st.session_state["run"] = client.beta.threads.runs.create(
        thread_id=st.session_state["thread"].id,
        assistant_id=st.session_state["assistant"].id,
    )

    completed = False

    while not completed:
        run = client.beta.threads.runs.retrieve(
            thread_id=st.session_state["thread"].id,
            run_id=st.session_state["run"].id,
        )

        if run.status == "completed":
            completed = True


        if run.status.required_action.submit_tool_outputs and run.status.required_action.submit_tool_outputs.tool_calls:
            print("toolCalls present:")
            toolCalls = run.status.required_action.submit_tool_outputs.tool_calls

            tool_outputs = []
            for toolcall in toolCalls:
                function_name = toolcall.function.name
                function_args = json.loads(toolcall.function.arguments)
                
                if function_name in tool_to_funtion:
                    
                    function_to_call = tool_to_funtion[function_name]

                    print(function_to_call,function_to_call.__name__=="update_map","================================================================")
                  
                    if function_to_call.__name__ == "update_map":
                        
                        response = function_to_call(
                        longitude=function_args.get("longitude"),
                        latitude=function_args.get("latitude"),
                        zoom= function_args.get("zoom")
                        )
                        
                        
                        tool_outputs.append({
                                  "tool_call_id": toolcall.id,
                                  "output": response
                              })
                    
            print(tool_outputs,">>>>>") 
            # Submit tool outputs and update the run
            client.beta.threads.runs.submit_tool_outputs(
                thread_id=st.session_state["thread"].id,
                run_id=st.session_state['run'].id,
                tool_outputs=tool_outputs)

        else:
            time.sleep(0.1)

    st.session_state["conversation"]= [
        ({'role':m.role, 'message':m.content[0].text.value})
        for m in client.beta.threads.messages.list(st.session_state["thread"].id).data
    ]
