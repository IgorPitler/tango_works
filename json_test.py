#v2
import json
import time

try:
    with open('example_json.txt', 'r') as file:
        json_example = file.read()
        #print(json_example)
except FileNotFoundError as e:
    print("File read error")


# test if all is ok!
try:
    data = json.loads(json_example)
except Exception as e:
    print("decode error!")



print(len(data['phoneNumbers']))
print(data['phoneNumbers'][0]['number'])

start_time = time.perf_counter()
# Your code here
#for i in range(1000000):
#    pass

end_time = time.perf_counter()
print(f"Execution time: {end_time - start_time:.7f} seconds")

print("json test ok")