import os
import sys
from deepface import DeepFace

def save(user_id):
    images = [ f.name for f in os.scandir("uploads/face") if f.is_dir()]
    os.rename("test.jpeg", f"uploads/face/{str(user_id)}/{len(images)+1}.jpeg")


def face_distance(user_id):
    user_ids = [ f.name for f in os.scandir("uploads/face") if f.is_dir()]
    if str(user_id) in user_ids:
        result = DeepFace.verify(img1_path = f"test.jpeg", img2_path = f"uploads/face/{str(user_id)}/1.jpeg", distance_metric = "cosine", enforce_detection=False)
        print("Face Recognition Distance: ", result['distance'])
        return result['distance']
    else:
        os.mkdir(f"uploads/face/{str(user_id)}")
        os.rename("test.jpeg", f"uploads/face/{str(user_id)}/1.jpeg")
        return 1


if __name__=="__main__":
    face_distance(1)