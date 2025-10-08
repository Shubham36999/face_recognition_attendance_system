from recognize import FaceRecognizer
import pickle, os, numpy as np
from deepface import DeepFace

def precompute_embeddings():
    embeddings_file = "embeddings.pkl"
    if os.path.exists(embeddings_file):
        print("✅ Embeddings already exist.")
        return

    known_faces_dir = "known_faces"
    embeddings_data = {}

    for person in os.listdir(known_faces_dir):
        person_dir = os.path.join(known_faces_dir, person)
        person_embeddings = []
        for img_file in os.listdir(person_dir):
            if img_file.lower().endswith((".jpg", ".jpeg", ".png")):
                img_path = os.path.join(person_dir, img_file)
                try:
                    emb = DeepFace.represent(img_path, model_name="VGG-Face", enforce_detection=False)
                    if emb and len(emb) > 0:
                        person_embeddings.append(emb[0]["embedding"])
                except:
                    continue
        if person_embeddings:
            embeddings_data[person] = np.mean(person_embeddings, axis=0)

    with open(embeddings_file, "wb") as f:
        pickle.dump(embeddings_data, f)
    print("🎯 Embeddings precomputed successfully.")

precompute_embeddings()
