from src.agent.tools.writing_tool import WritingTool

writing_tool = WritingTool()

print(writing_tool.name())
print(writing_tool.description())
print(writing_tool.config["system_instruction"])
print(writing_tool.use("some warnings"))
# warning = "The temperature is 6C. Which is under the threshold of 10C"
# context = "In Brussels today is frrezing with temperatures of 0°C"
#
# print(writing_tool.use(warning, context))
