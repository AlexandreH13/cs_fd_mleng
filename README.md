## CS_FD_MLENG - A simple case

**Description**

This repo is a case of how to productionize a machine learning model for fraud detection.

---

**How to run**

For now **the case is in development**. The sugestion is to build the docker image and run the container.

```bash
docker build -t project_tag .
```

After that, you can run the container with the following command:

```bash
docker run -it image_name
```

NOTE: The model is currently persisted in the `artifacts` folder.