module.exports = {view_set: function(router, url, model, serializer=null) {
    if(serializer === null) {
        serializer = {
            to_json: (val) => val,
            from_req: async (req) => req.body,
        }
    }

    const update = async (req, res) => {
        //try {
            serializer.from_req(req, async (data) => {
                await model.updateOne({_id: req.params.id}, {'$set': data})
                const post = await model.findOne({_id: req.params.id})
                res.send(post)
            });
       //} catch {
       //    res.status(404)
       //    res.send({error: "model doesn't exist!"})
       //}
    }
    const remove = async (req, res) => {
        try {
            await model.deleteOne({_id: req.params.id})
            res.status(204).send()
        } catch {
            res.status(404)
            res.send({error: "model doesn't exist!"})
        }
    }
    const get_one = async (req, res) => {
        try {
            const post = await model.findOne({_id: req.params.id});
            res.send(serializer.to_json(post));
        } catch {
            res.status(404)
            res.send({error: "model doesn't exist!"})
        }
    }
    const create = async (req, res) => {
        serializer.from_req(req, async (data) => {
            const post = new model(data)
            await post.save()
            res.send(post)
        });
    }
    router.get(url, async (req, res) => {
        let filters = req.query.filter?JSON.parse(req.query.filter):{};
        Object.keys(filters).forEach(k => {
           filters[k] = {'$regex': filters[k], '$options': 1}
        });
        let sort=(req.query.sort!=='id')?req.query.sort:'_id';
        let total = await model.countDocuments(filters);
        let start = (req.query.page-1)*req.query.perPage;
        let posts = await model.find(filters).sort({sort: (req.query.order==='ASC')?1:-1}).skip(start).limit(req.query.perPage);
        res.header('Content-Range', `${url} ${start}-${start+posts.length}/${total}`);
        res.json(posts)//.map(serializer.to_json));
    })

    router.post(url, create)

    router.get(url + "/:id", get_one)

    router.patch(url + "/:id", update)
    router.put(url + "/:id", update)


    router.delete(url + "/:id", remove)

}
}