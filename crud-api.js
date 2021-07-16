module.exports = {view_set: function(router, url, model) {

    router.get(url, async (req, res) => {
        let filters = req.query.filter?JSON.parse(req.query.filter):{};
        Object.keys(filters).forEach(k => {
           filters[k] = {'$regex': filters[k], '$options': 1}
        });
        let sort=(req.query.sort!=='id')?req.query.sort:'_id';
        let total = await model.countDocuments(filters);
        let start = (req.query.page-1)*req.query.perPage;
        let posts = await model.find(filters).sort({sort: (req.query.order==='ASC')?1:-1}).skip(start).limit(req.query.perPage);
        posts = [...posts];
        res.header('Content-Range', `${url} ${start}-${start+posts.length}/${total}`);
        res.json(posts);
    })

    router.post(url, async (req, res) => {
        const post = new model(req.body)
        await post.save()
        res.send(post)
    })

    router.get(url + "/:id", async (req, res) => {
        try {
            const post = await model.findOne({_id: req.params.id})
            res.send(post)
        } catch {
            res.status(404)
            res.send({error: "model doesn't exist!"})
        }
    })

    router.patch(url + "/:id", async (req, res) => {
        try {
            const post = await model.findOne({_id: req.params.id})
            for(let k in req.body) {
                if (k.indexOf('_') !== 0) {
                    post[k] = req.body[k];
                }
            }

            await post.save()
            res.send(post)
        } catch {
            res.status(404)
            res.send({error: "model doesn't exist!"})
        }
    })

    router.put(url + "/:id", async (req, res) => {
        try {
            const post = await model.findOne({_id: req.params.id})
            for(let k in req.body) {
                if (k.indexOf('_') !== 0) {
                    post[k] = req.body[k];
                }
            }

            await post.save()
            res.send(post)
        } catch {
            res.status(404)
            res.send({error: "model doesn't exist!"})
        }
    })

    router.delete(url + "/:id", async (req, res) => {
        try {
            await model.deleteOne({_id: req.params.id})
            res.status(204).send()
        } catch {
            res.status(404)
            res.send({error: "model doesn't exist!"})
        }
    })

}
}