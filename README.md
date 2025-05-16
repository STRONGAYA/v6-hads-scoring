# Vantage6 HADS scoring algorithm

## What does this algorithm do?

This Vantage6 algorithm performs HADS scoring and computes the scores general
statistics.  
It allows users to specify the module and the domain of interest;
optionally, users can also specify a variable to stratify the dataset on.

The algorithm incorporates various functionalities,
consisting of: general data processing, privacy-enhancing measures,
score computation, and general statistics computation thereof.

For a more detailed description of the algorithm, please refer to
the associated [Wiki](https://github.com/STRONGAYA/v6-hads-scoring/wiki).

## How to use this algorithm?

This algorithm is designed to be run with the [vantage6](https://vantage6.ai) infrastructure for distributed analysis
and learning.  
Please refer to the [Wiki](https://github.com/STRONGAYA/v6-hads-scoring/wiki)
on how the algorithm is exactly to be used.

The base code for this algorithm has been created via
the [v6-algorithm-template](https://github.com/vantage6/v6-algorithm-template) template generator.

## Creating your own version?

If you want to create your own version of this algorithm,
you can do so by forking or cloning the repository and follow the following steps:

### Dockerizing your algorithm

To finally run your algorithm on the vantage6 infrastructure, you need to
create a Docker image of your algorithm.

#### Automatically

The easiest way to create a Docker image is to use the GitHub Actions pipeline to
automatically build and push the Docker image. All that you need to do is push a
commit to the ``main`` branch.

#### Manually

A Docker image can be created by executing the following command in the root of your
algorithm directory:

```bash
docker build -t [my_docker_image_name] .
```

where you should provide a sensible value for the Docker image name.
The `docker build` command will create a Docker image that contains your algorithm.
You can create an additional tag for it by running:

```bash
docker tag [my_docker_image_name] [another_image_name]
```

This way, you can e.g. do `docker tag local_average_algorithm harbor2.vantage6.ai/algorithms/average`
to make the algorithm available on a remote Docker registry (in this case `harbor2.vantage6.ai`).

Finally, you need to push the image to the Docker registry.
This can be done by running:

```bash
docker push [my_docker_image_name]
```

Note that you need to be logged in to the Docker registry before you can push
the image. You can do this by running `docker login` and providing your
credentials. Check [this page](https://docs.docker.com/get-started/04_sharing_app/)
For more details on sharing images on Docker Hub. If you are using a different
Docker registry, check the documentation of that registry and be sure that you
have sufficient permissions.