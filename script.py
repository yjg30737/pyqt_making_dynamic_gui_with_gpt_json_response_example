import copy

from openai import OpenAI

JSON_RESPONSE_DICT = {
    "anything": {
        "query": "List of {}: {}\n"
                 "Return following JSON object by according to {} above.",
        "json_format": {
            "Description": {}
        }
    }
}

class GPTJsonWrapper:
    def __init__(self, api_key=None):
        super().__init__()
        # Initialize OpenAI client
        if api_key:
            self.__client = OpenAI(api_key=api_key)
        self.__topic = ''
        self.__rows = []
        self.__columns = []

    def set_api(self, api_key):
        self.__api_key = api_key
        self.__client = OpenAI(api_key=api_key)

    def set_topic(self, topic: str):
        self.__topic = topic

    def set_columns(self, columns: list):
        self.__columns = columns

    def set_rows(self, rows: list):
        self.__rows = rows

    def get_data(self):
        cur_obj = copy.deepcopy(JSON_RESPONSE_DICT["anything"])
        cur_obj["query"] = cur_obj["query"].format(
            self.__topic, self.__rows, self.__topic
        )

        for _ in self.__columns:
            cur_obj['json_format'].update({_: []})

        return eval(self.get_response(response_format="json_object", objective=cur_obj))


    def get_response(
        self,
        model="gpt-4-1106-preview",
        n=1,
        temperature=1,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        response_format="text",
        objective: dict = {},
        stream=False,
    ):
        query = objective["query"] + " " + str(objective["json_format"])
        try:
            openai_arg = {
                "model": model,
                "messages": [],
                "n": n,
                "temperature": temperature,
                "top_p": top_p,
                "frequency_penalty": frequency_penalty,
                "presence_penalty": presence_penalty,
                "stream": stream,
                "response_format": {"type": response_format},
            }

            openai_arg["messages"].append({"role": "user", "content": query})

            response = self.__client.chat.completions.create(**openai_arg)
            response_content = response.choices[0].message.content

            return response_content
        except Exception as e:
            print(e)