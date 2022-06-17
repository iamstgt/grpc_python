import json
import user_pb2_grpc
import user_pb2
import grpc
from concurrent.futures import ThreadPoolExecutor


# Load user info
with open("users.json") as f:
    users = json.load(f)


class UserManager(user_pb2_grpc.UserManagerServicer):
    def get(self, request, context):
        user_id = request.id

        if str(user_id) not in users:
            return user_pb2.UserResponse(error=True, mesage="Not found")

        user = users[str(user_id)]

        result = user_pb2.User()
        result.id = user["id"]
        result.name = user["name"]
        result.email = user["email"]
        result.user_type = user_pb2.User.UserType.Value(user["user_type"])

        return user_pb2.UserResponse(error=False, user=result)


def main():
    # Create server object
    server = grpc.server(ThreadPoolExecutor(max_workers=2))
    # Set service to server object
    user_pb2_grpc.add_UserManagerServicer_to_server(UserManager(), server)
    # Designate address and port
    server.add_insecure_port('[::]:1234')
    # Waite for client request
    server.start()
    # Terminate after receiving a request
    server.wait_for_termination()


if __name__ == '__main__':
    main()


