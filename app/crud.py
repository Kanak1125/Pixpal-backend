import json
# from datetime import datetime

from sqlalchemy.orm import Session, joinedload

from . import models, schemas

COLOR_RANGE = {
    "red": '{0}'.format(range(0, 60)),
    "yellow": '{0}'.format(range(60, 120)),
    "green": '{0}'.format(range(120, 180)),
    "cyan": '{0}'.format(range(180, 240)),
    "blue": '{0}'.format(range(240, 300)),
    "magenta": '{0}'.format(range(300, 360)),
}
## Singleton pattern

def get_or_create_color(db: Session, color_data: schemas.Color):
    '''
        function to add color data to the db...
    '''
    color = db.query(models.Color).filter_by(
        hue = color_data.hue,
        saturation = color_data.saturation,
        value = color_data.value
    ).first()

    if color is None:
        color = models.Color(
            hue = color_data.hue,
            saturation = color_data.saturation,
            value = color_data.value
        )

        db.add(color)
        db.commit()
        db.refresh(color)

    return color

def get_image(db: Session, image_id: int):
    result = db.query(models.Image).filter(models.Image.id == image_id).first()
    # response = {
    #     json.dumps(result)
    # }
    return result

def get_images(skip: int, limit: int, db: Session):
    # return db.query(models.Image).options(joinedload(models.Image.user_id)).all()
    # query = (db.query(models.Image)).compile(dialect=postgresql.dialect, compile_kwargs={"literal_binds": True})

    print("QUERY ----->", db.query(models.Image))
    print("\n\n\n\nValue of skip ----->", skip, "\n\n\n\nValue of limit----->", limit)

    return db.query(models.Image).offset(skip).limit(limit).options(joinedload(models.Image.tags)).all()

def get_images_searches(db: Session, **query_str):
    print("QUERY ----->", db.query(models.Image))

    search_query = query_str["q"]
    orientation_query = query_str["orientation"]
    color_query = query_str["color"]
    file_type_query = query_str["file_type"]

    image_query = db.query(models.Image).filter(models.Image.tags.any(models.Tag.title.in_(search_query)))

    if "all" in search_query:
        image_query = db.query(models.Image)

    if not search_query:
        return []
    
    # query_tags = db.query(models.Tag).filter(models.Tag.title.in_(search_query)).all()

    print("IMGQUERY 1 ", image_query.count(), "\n\n\n\n\n\n")
    
    if orientation_query:
        match (orientation_query):
            case 'landscape':

                image_query = image_query.filter(models.Image.height < models.Image.width)
            
            case 'portrait':
                image_query = image_query.filter(models.Image.height > models.Image.width)

            case 'square':
                image_query = image_query.filter(models.Image.height == models.Image.width)

            case 'panaromic':
                pass

    if file_type_query:
        image_query = image_query.filter(models.Image.file_name.contains(f'.{file_type_query}'))

    if color_query:
        # image_query = image_query.filter(models.Image.color)
        print("\n\n\nData from the colored filter =======> {0} \n\n\n".format(image_query.filter(models.Image.color.contains(color_query))))
        pass
        # image_query = image_query.filter(models.Image.color[0] in COLOR_RANGE[color_query])

    # images = []
    # for image in image_query.all():
    #     images.extend(image)

    # unique_images = list(set(images))
    # print("UNIQUE IMAGES ====> ", unique_images)
    print("IMAGES FROM THE QUERY =====> ", image_query)
    
    return image_query.all()

def create_image(db: Session, image: schemas.ImageCreate):
    # instance of models.Image...

    color = get_or_create_color(db, image.average_color)
    
    tags = db.query(models.Tag).filter(models.Tag.id.in_(image.tags)).all()
    # tag1 = models.Tag(id=202, title="water", type="search")
    # tag2 = models.Tag(id=304, title="old", type="search")

    print("CREAATE IMAGE ", image.file_name, flush=True) 
    db_image = models.Image(blur_hash= image.blur_hash, 
                            # created_at= datetime.fromtimestamp(datetime.UTC), 
                            created_at= image.created_at, 
                            description= image.description, 
                            alt_description= image.alt_description, width= image.width, height = image.height, average_color_id = color.id, likes = image.likes, file_name= image.file_name, user_id= 1, tags=tags)
    ## tags = image.tags
    ### tags = tags
    # db_image.tags.add_all()

    # tags and url to be included....
    
    # response = {
    #     "id": db_image.id,
    #     "blur_hash": db_image.blur_hash,
    #     "created_at": db_image.created_at,
    #     "description": db_image.description,
    #     "alt_description": db_image.alt_description,
    #     "width": db_image.width,
    #     "height": db_image.height,
    #     "color": db_image.color,
    #     "likes": db_image.likes,
    #     "user": {
    #         "id": db_image.user.id,
    #         "username": db_image.user.username,
    #         "email": db_image.user.email,
    #     }
    # )

    # for tag in tags:
    #     db_image.tags.append(tag)

    db.add(db_image)
    db.commit()
    db.refresh(db_image)


    return db_image

def get_tag(db: Session, tag_id: int):
    return db.query(models.Tag).filter(models.Tag.id == tag_id).first()

def get_tags(db: Session):
    return db.query(models.Tag).options(joinedload(models.Tag.images)).all()

def create_tag(db: Session, tag: schemas.TagCreate):
    db_tag = models.Tag(title=tag.title, type=tag.type)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(first_name=user.first_name, last_name= user.last_name, username= user.username, profile_image_url= user.profile_image_url, email= user.email, password= user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user